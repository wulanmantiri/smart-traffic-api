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
        green_lane_history = event_body['green_lane_history']
        config = event_body['config']
    except KeyError as e:
        return format_error_resp(f'Payload [{str(e)}] is required.')
    except Exception as e:
        return format_error_resp(f'Error {str(e)} occurred.')

    min_green_time = config.get('min_green_time', 10)
    max_green_time = config.get('max_green_time', 60)
    ratio_time = config.get('ratio_time', 1)
    ratio_vehicle = config.get('ratio_vehicle', 1)
    enable_stream = config.get('enable_stream', True)

    max_score = 0
    max_prob = 0
    green_lane = None
    num_of_lanes = len(lanes)
    score_details = []
    for lane_id in range(num_of_lanes):
        try:
            prob = (green_lane_history.index(lane_id) + 1) / num_of_lanes
        except:
            prob = 1

        vehicle_count = lanes[lane_id]['count']
        score = prob * vehicle_count
        if score > max_score or (score == max_score and prob > max_prob):
            max_score = score
            max_prob = prob
            green_lane = lane_id

        score_details.append(f'{prob:.2f} ✕ {vehicle_count} = {score:.2f}')

    green_lane_count = lanes[green_lane]['count']
    actual_green_time = round(green_lane_count * ratio_time / ratio_vehicle)
    green_time = max([actual_green_time, min_green_time])
    green_time = min([green_time, max_green_time])
    green_lane_details = {
        'lane': green_lane,
        'calc_time': green_time,
        'actual_time_details': f'{green_lane_count} ✕ ({ratio_time}/{ratio_vehicle}) = {actual_green_time}'
    }

    if green_lane in green_lane_history:
        green_lane_history.remove(green_lane)
    green_lane_history.insert(0, green_lane)

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
        'green_lane_history': green_lane_history,
    }
    return format_success_resp(response_body)
