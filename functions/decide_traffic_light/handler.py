import json
import boto3
import os


RESPONSE_HEADERS =  {
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
}


def format_error_resp(error_message, status_code=400):
    return {
        'statusCode': status_code,
        'headers': RESPONSE_HEADERS,
        'body': json.dumps({
            'error': error_message,
        }),
    }


def format_success_resp(response_body, status_code=200):
    return {
        'statusCode': status_code,
        'headers': RESPONSE_HEADERS,
        'body': json.dumps(response_body),
    }


def decide_traffic_light(event, _):
    try:
        event_body = json.loads(event['body'])
        lanes = event_body['lanes']
        history = event_body['history']
        config = event_body['config']
    except KeyError as e:
        return format_error_resp(f'Payload [{str(e)}] is required.')
    except Exception as e:
        return format_error_resp(f'Error {str(e)} occurred.')

    num_of_lanes = len(lanes)
    consecutive_red_turns = event_body.get('consecutive_red_turns', [0] * num_of_lanes)

    min_green_time = config.get('min_green_time', 10)
    max_green_time = config.get('max_green_time', 60)
    ratio_time = config.get('ratio_time', 1)
    ratio_vehicle = config.get('ratio_vehicle', 1)
    enable_stream = config.get('enable_stream', True)

    # Traffic lanes that exceed max consecutive red light threshold and have at least 1 queueing vehicle
    # Current threshold = num of lanes
    prioritized_lanes = [
        lane_id
        for lane_id, red_turns in enumerate(consecutive_red_turns)
        if red_turns >= num_of_lanes and lanes[lane_id]['total_count'] > 0
    ]

    max_score = 0
    max_prob = 0
    green_lane = None
    score_details = []
    for lane_id in range(num_of_lanes):
        # Calculate probability
        try:
            prob = (history.index(lane_id) + 1) / (num_of_lanes + 1)
        except:
            prob = 1
        if len(prioritized_lanes) > 0 and lane_id not in prioritized_lanes:
            prob = 0

        vehicle_count = lanes[lane_id]['total_count']
        score = prob * vehicle_count
        if score > max_score or (score == max_score and prob > max_prob):
            max_score = score
            max_prob = prob
            green_lane = lane_id

        score_details.append(f'{prob:.2f} ✕ {vehicle_count} = {score:.2f}')

    green_lane_count = lanes[green_lane]['total_count']
    actual_green_time = round(green_lane_count * ratio_time / ratio_vehicle)
    green_time = max([actual_green_time, min_green_time])
    green_time = min([green_time, max_green_time])
    green_lane_details = {
        'lane': green_lane,
        'calc_time': green_time,
        'actual_time_details': f'{green_lane_count} ✕ ({ratio_time}/{ratio_vehicle}) = {actual_green_time}',
    }

    new_consecutive_red_turns = []
    for lane_id, red_turns in enumerate(consecutive_red_turns):
        new_consecutive_red_turns.append(red_turns + 1 if lane_id != green_lane else 0)

    # Store data in S3 via Kinesis Firehose
    if enable_stream:
        firehose_client = boto3.client('firehose')
        stream_name = os.environ.get('DELIVERY_STREAM_NAME')
        firehose_client.put_record_batch(
            DeliveryStreamName=stream_name,
            Records=[
                {
                    'Data': json.dumps(lanes)
                },
            ]
        )

    response_body = {
        'score_details': score_details,
        'green': green_lane_details,
        'history': history,
        'consecutive_red_turns': new_consecutive_red_turns,
    }
    return format_success_resp(response_body)
