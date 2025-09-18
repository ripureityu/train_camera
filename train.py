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
def disconnect(msg):
    print("message: ", msg)

eio.connect("http://localhost:3000", transports=["polling"])
# カメラを開く
cap = cv2.VideoCapture(0)
# 画像をキャプチャする
ret, frame = cap.read()
#return ,image
if ret == True:
    cv2.imwrite("image.jpg", frame)
else:
    print("---カメラから画像を取得できませんでした---")
# カメラを閉じる
cap.release()
eio.wait()

