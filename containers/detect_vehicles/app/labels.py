import os
from .constants import CLASS_FILE_ABS_PATH


def populate_common_labels():
    """A method to obtain class labels for model based on CLASS_* configuration"""

    if not os.path.exists(CLASS_FILE_ABS_PATH):
        raise FileNotFoundError(f'{CLASS_FILE_ABS_PATH} does not exist.')

    f = open(CLASS_FILE_ABS_PATH, 'r')
    classes = [line.strip() for line in f.readlines()]
    return classes


def count_vehicle_labels(labels):
    res = {
        'car': 0,
        'truck': 0,
        'motorbike': 0,
        'bus': 0,
    }
    for name in labels:
        try:
            res[name] += 1
        except KeyError:
            pass
    res['total'] = sum(res.values())
    return res
