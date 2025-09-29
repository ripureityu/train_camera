import cv2
import engineio

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
    if msg == " picture request":
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        _,buf =cv2.imencode('.jpg', frame)
        eio.send(buf.tobytes())#画像をバイナリで送信
        eio.send("crossing_send")
        print("画像データを送信しました")
    elif msg == "stop picture":
        cap.release()


eio.connect("http://localhost:3000", transports=["polling"])

eio.wait()
