import engineio           # リアルタイム通信用
import flask              # Webサーバ用
import waitress           # WSGIサーバ用

app = flask.Flask(__name__)

eio = engineio.Server(
    allow_upgrades=False,
    transports=["polling"],  # WebSocketを使わずpollingのみ
)

sidlist = {}  # 踏切ごとのセッションID管理

@eio.on("connect")
def connect(sid, environ):
    print("Connected: ", sid)  # クライアント接続時

@eio.on("disconnect")
def disconnect(sid):
    sidlist.append(sid)        # 切断時（本来は削除が正しい）
    print("Disconnected:", sid)

@eio.on("message")
def message(sid, msg):
    # crossing-id受信時は踏切IDとセッションIDを紐付け
    if msg.startswith("crossing-id "):
        sp = msg.split()
        crossing_id = sp[1]
        sidlist[crossing_id] = sid
    elif msg == "crossing_send":
        # 画像データ受信処理（未使用）
        with open("cross.png", "wb") as f:
            img = eio.receive(sid)
            pictute =  f.write(msg)
            eio.send()   

@app.route("/vigcamera", methods=["GET"])
def index():
    # 列車側から踏切カメラに撮影リクエスト
    crossing_id = flask.request.args.get("crossing-id","")
    print("vigcamera", crossing_id)
    sid  = sidlist[crossing_id]
    eio.send(sid,"picture request")  # 踏切カメラにリクエスト送信
    return "send ok"

picture_data = {}  # crossing-idごとの画像データ保存

@app.route("/picture", methods=["POST"])
def picture():
    # 踏切カメラから画像データ受信
    crossing_id = flask.request.args.get("crossing-id","")
    print("picture", crossing_id)
    data = flask.request.get_data()
    picture_data[crossing_id] = data    
    return "ok"

@app.route("/get_picture", methods=["GET"])
def get_picture():
    # 列車側から画像データ取得
    crossing_id = flask.request.args.get("crossing-id","")
    print("get_picture", crossing_id)
    data = picture_data[crossing_id]   
    return data

if __name__ == "__main__":
    waitressapp = engineio.WSGIApp(eio, wsgi_app=app)
    waitress.serve(
        waitressapp,
        host="0.0.0.0",
        port=3000,
    )