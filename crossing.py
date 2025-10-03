import cv2
import engineio
import requests

cap = cv2.VideoCapture(0)

# import http.client
# http.client.HTTPConnection.debuglevel = 1
eio = engineio.Client(
    # logger=True,
)

@eio.on("connect")
def connect():
    print("connect")
    eio.send("crossing-id test1")

@eio.on("disconnect")
def disconnect():
    print("disconnect")

@eio.on("message")
def message(msg):
    print("message:", msg)
    if msg == "picture request":
        ret, frame = cap.read()
        _, buf = cv2.imencode('.png', frame)
        buf = buf.tobytes()
        response = requests.post(
            url="http://localhost:3000/picture",
            data=buf,
           
           
            params={"crossing-id":"test1"},
        )
        print("画像データを送信しました")

        


eio.connect("http://localhost:3000", transports=["polling"])

eio.wait()
