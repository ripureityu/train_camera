import cv2
import numpy as np
from ultralytics import YOLO

# Load a pre-trained YOLO model (adjust model type as needed)
model = YOLO("yolo11n.pt")  # n, s, m, l, x versions available

# Perform object detection on an image

def t_f(picture_data):
    results = model.predict(source=picture_data)  # Can also use video, directory, URL, etc.
    result = results[0]
    aaa =result.summary()
    print(aaa)
    for i in aaa:
        value = i['name']
        if value == 'person':
            return True
    return False
f =open("bus.jpg","rb") 
print(f)
fa =f.read()#圧縮されている
bbb = cv2.imdecode(np.frombuffer(fa,np.uint8),cv2.IMREAD_COLOR_BGR)#圧縮されていない
print(fa)
data = t_f(bbb)
print(data)
f.close()

'''
[
    {'name': 'bus', 'class': 5, 'confidence': 0.94015, 'box': {'x1': 3.83267, 'y1': 229.3642, 'x2': 796.19458, 'y2': 728.41223}},
    {'name': 'person', 'class': 0, 'confidence': 0.88822, 'box': {'x1': 671.01721, 'y1': 394.83319, 'x2': 809.80975, 'y2': 878.71246}}, 
    {'name': 'person', 'class': 0, 'confidence': 0.87825, 'box': {'x1': 47.40473, 'y1': 399.56512, 'x2': 239.30066, 'y2': 904.19501}}, 
    {'name': 'person', 'class': 0, 'confidence': 0.85577, 'box': {'x1': 223.05894, 'y1': 408.68866, 'x2': 344.46768, 'y2': 860.43579}},
    {'name': 'person', 'class': 0, 'confidence': 0.62192, 'box': {'x1': 0.02174, 'y1': 556.06854, 'x2': 68.88548, 'y2': 872.35919}}
]
'''


 


 model = YOLO("yolo11n.pt")

def t_f(picture_data):
    results = model.predict(source=picture_data)  # Can also use video, directory, URL, etc.
    result = results[0]
    aaa =result.summary()
    print(aaa)
    for i in aaa:
        value = i['name']
        if value == 'person':
            return True
    return False