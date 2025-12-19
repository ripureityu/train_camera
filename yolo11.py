import cv2
from ultralytics.models.yolo import YOLO

# YOLOv11のモデルをロード
model = YOLO("yolo11n.pt") 


def cls():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    results = model.predict(frame)
    boxes = results[0].boxes
    if boxes is None:
        return "error"
    boxes_cls = boxes.cls.tolist()
    print(boxes_cls)
cls()


    
'''
boxes_cls = [5, 0, 1, 2, 0]
    for box in range(len(boxes_cls)):
        if boxes_cls[box] == 0 or boxes_cls[box] == 2:
            return "person_car"
    return "not person_car"
'''
