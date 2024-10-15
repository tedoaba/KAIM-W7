import torch
import cv2
from yolov5.models.common import DetectMultiBackend

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = DetectMultiBackend('../yolov5/yolov5s.pt', device=device)

def detect_objects(image_path):
    img = cv2.imread(image_path)
    results = model(img)
    detections = []
    for *box, conf, cls in results.xyxy[0]:
        detections.append({
            'bounding_box': str(box),
            'confidence': conf.item(),
            'label': model.names[int(cls)]
        })
    return detections
