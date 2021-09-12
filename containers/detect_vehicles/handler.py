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

    confidence = event_body.get('confidence', 0.21)
    nms_thresh = event_body.get('nms_threshold', 0.5)
    blob_size = 416

    imageb64_size = len(image_base64) * 3 / 4
    if imageb64_size > 1048576: # image is more than 1MB
        if event_body.get('prioritize_quantity', False):
            blob_size = 1280
            confidence = 0.1

    image = decode_image(image_base64)
    box, labels, count = detect_common_objects(
        image,
        confidence=confidence, 
        nms_thresh=nms_thresh,
        size=blob_size,
    )

    response_body = {
        'count': count_vehicle_labels(labels),
        'image': None,
    }
    if return_bbox_image:
        output_image = draw_bbox(image, box, labels, count)
        response_body['image'] = encode_image(output_image)

    return format_success_resp(response_body)
