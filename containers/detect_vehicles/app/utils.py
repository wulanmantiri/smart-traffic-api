import base64
import numpy as np
import cv2
import json

from .constants import RESPONSE_HEADERS


def decode_image(img_base64):
    img_str = base64.b64decode(img_base64)
    img_as_np = np.frombuffer(img_str, dtype=np.uint8)
    return cv2.imdecode(img_as_np, flags=1)


def encode_image(image):
    _, buffer = cv2.imencode('.jpg', image)
    img_bytes = base64.b64encode(buffer)
    return img_bytes.decode()


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
