FROM public.ecr.aws/lambda/python:3.9

ARG MODEL_DIR="/smart-traffic/model"
RUN mkdir -p ${MODEL_DIR}

ADD https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg ${MODEL_DIR}/yolov4.cfg
ADD https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names ${MODEL_DIR}/coco_classes.txt
RUN curl -L https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights -o ${MODEL_DIR}/yolov4.weights

RUN chmod 644 $(find ${MODEL_DIR} -type f)
RUN chmod 755 $(find ${MODEL_DIR} -type d)

COPY requirements.txt requirements.txt
RUN pip3 install --target ${LAMBDA_TASK_ROOT} -r requirements.txt

COPY app app
COPY handler.py handler.py

CMD [ "handler.detect_vehicles" ]
