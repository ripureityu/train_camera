import cv2                 # カメラ画像取得用
import engineio            # リアルタイム通信用
import requests            # HTTP通信用
from ultralytics.models.yolo import YOLO

model = YOLO("yolo11n.pt") # YOLOv11のモデルをロード
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
        # cap.read() の戻り値を必ずチェックし、frame が None または空画像 の場合は送信しない
        try:
            # カメラが閉じている場合は再オープンを試みる
            global cap
            if not cap or not cap.isOpened():
                try:
                    cap.release()
                except Exception:
                    pass
                cap = cv2.VideoCapture(0)

            ret, frame = cap.read()
        except Exception as e:
            print("cap.read() エラー:", e)
            return

        # フレームが正しいか厳密にチェック
        if not ret or frame is None:
            print("カメラ読み取り失敗またはフレームが None。画像を送信しません。")
            return
        # フレームが空配列の場合をチェック
        if not hasattr(frame, "size") or frame.size == 0:
            print("フレームが空です。送信を中止します。")
            return
        # 形状チェック（高さ/幅がゼロでないこと）
        try:
            h, w = frame.shape[:2]
            if h == 0 or w == 0:
                print("フレームの幅または高さが0です。送信を中止します。")
                return
        except Exception:
            # shape が取得できない場合も送信中止
            print("フレームの shape を取得できません。送信を中止します。")
            return

        # PNG へエンコードは例外を投げる可能性があるため try/except で保護
        try:
            success, buf = cv2.imencode('.png', frame)
        except cv2.error as e:
            print("cv2.imencode エラー:", e)
            return
        except Exception as e:
            print("画像エンコード時の予期せぬエラー:", e)
            return

        if not success or buf is None:
            print("画像エンコード失敗。送信しません。")
            return

        data = buf.tobytes()

        # 画像データをサーバに送信
        try:
            response = requests.post(
                url="http://localhost:3000/picture",
                data=data,
                params={"crossing-id":"test1"},
                timeout=5
            )
            print("画像データを送信しました. status:", response.status_code)
        except Exception as e:
            print("画像送信エラー:", e)

# サーバに接続
try:
    eio.connect("http://localhost:3000", transports=["polling"])
    eio.wait()  # イベントループ
except Exception as e:
    print("Engine.IO 接続エラー:", e)