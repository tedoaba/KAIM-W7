import torch
import cv2
import sys
import os
from pathlib import Path

# Import the necessary modules
from yolov5.models.common import AutoShape, DetectMultiBackend

# Load the YOLOv5 model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = DetectMultiBackend('../yolov5/yolov5s.pt', device=device)


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
