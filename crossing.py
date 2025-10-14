import cv2                 # カメラ画像取得用
import engineio            # リアルタイム通信用
import requests            # HTTP通信用

cap = cv2.VideoCapture(0)  # カメラデバイスを開く

eio = engineio.Client()    # Engine.IOクライアント生成

@eio.on("connect")
def connect():
    print("connect")
    eio.send("crossing-id test1")  # 踏切IDをサーバに通知

@eio.on("disconnect")
def disconnect():
    print("disconnect")

@eio.on("message")
def message(msg):
    print("message:", msg)
    if msg == "picture request":
        # サーバから撮影リクエストを受けたら画像を撮影
        ret, frame = cap.read()
        _, buf = cv2.imencode('.png', frame)  # PNG形式に変換
        buf = buf.tobytes()                   # バイナリデータ化
        response = requests.post(
            url="http://localhost:3000/picture",
            data=buf,
            params={"crossing-id":"test1"},
        )
        print("画像データを送信しました")

eio.connect("http://localhost:3000", transports=["polling"])  # サーバに接続
eio.wait()  # イベント