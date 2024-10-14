import torch
import cv2
import sys
import os

# Add the YOLOv5 directory to the Python path
yolov5_dir = os.path.join(os.path.dirname(__file__), "yolov5")
sys.path.append(yolov5_dir)

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload=True)


def detect_objects(image_path):
    # Load image
    img = cv2.imread(image_path)

    # Perform object detection
    results = model(img)

    # Extract relevant information
    detections = []
    for *box, conf, cls in results.xyxy[0]:
        detections.append({
            'bounding_box': box,
            'confidence': conf.item(),
            'label': model.names[int(cls)]
        })
    return detections
