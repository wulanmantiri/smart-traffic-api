import json

from app.detect_objects import detect_common_objects, draw_bbox
from app.labels import count_vehicle_labels
from app.utils import decode_image, encode_image, format_error_resp, format_success_resp


def detect_vehicles(event, _):
    try:
        event_body = json.loads(event['body'])
        image_base64 = event_body['image']
        return_bbox_image = event_body['return_bbox_image']
    except KeyError as e:
        return format_error_resp(f'Payload {str(e)} is required.')

    image = decode_image(image_base64)
    box, labels, count = detect_common_objects(image)

    response_body = {
        'count': count_vehicle_labels(labels),
        'image': None,
    }
    if return_bbox_image:
        output_image = draw_bbox(image, box, labels, count)
        response_body['image'] = encode_image(output_image)

    return format_success_resp(response_body)
