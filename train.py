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

@eio.on("disconnect")
def disconnect():
    print("disconnect")

@eio.on("message")
def message(msg):
    print("message: ", msg)
    if msg == "capture":
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cv2.imwrite("capture.jpg", frame)
        print("capture.jpgを保存しました")
        cap.release()

eio.connect("http://localhost:3000", transports=["polling"])


eio.wait()


