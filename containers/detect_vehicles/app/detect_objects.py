import os
import cv2
import numpy as np

from .constants import CFG_FILE_ABS_PATH, WEIGHTS_FILE_ABS_PATH
from .labels import populate_common_labels


# Pre-populate class and color labels
classes = populate_common_labels()
COLORS = np.random.uniform(0, 255, size=(80, 3))


def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers


def draw_bbox(img, bbox, labels, confidence, colors=None, write_conf=False):
    """A method to apply a box to the image
    Args:
        img: An image in the form of a numPy array
        bbox: An array of bounding boxes
        labels: An array of labels
        colors: An array of colours the length of the number of targets(80)
        write_conf: An option to write the confidences to the image
    """
    for i, label in enumerate(labels):
        if colors is None:
            color = COLORS[classes.index(label)]            
        else:
            color = colors[classes.index(label)]

        if write_conf:
            label += ' ' + str(format(confidence[i] * 100, '.2f')) + '%'

        cv2.rectangle(img, (bbox[i][0],bbox[i][1]), (bbox[i][2],bbox[i][3]), color, 2)
        cv2.putText(img, label, (bbox[i][0],bbox[i][1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return img


def detect_common_objects(image, confidence=0.1, nms_thresh=0.5, size=1280):
    """A method to detect common objects (with most suitable default params)
    Args:
        image: A colour image in a numpy array
        confidence: A value to filter out objects recognised to a lower confidence score
        nms_thresh: An NMS value
        size: A blob size for width and height
        enable_gpu: A boolean to set whether the GPU will be used
    """

    height, width = image.shape[:2]
    scale = 0.00392
    blob = cv2.dnn.blobFromImage(image, scale, (size,size), (0,0,0), True, crop=False)

    net = cv2.dnn.readNet(WEIGHTS_FILE_ABS_PATH, CFG_FILE_ABS_PATH)
    net.setInput(blob)
    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            max_conf = scores[class_id]
            if max_conf > confidence:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = center_x - (w / 2)
                y = center_y - (h / 2)
                class_ids.append(class_id)
                confidences.append(float(max_conf))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence, nms_thresh)

    bbox = []
    label = []
    conf = []
    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        bbox.append([int(x), int(y), int(x+w), int(y+h)])
        label.append(str(classes[class_ids[i]]))
        conf.append(confidences[i])

    return bbox, label, conf
