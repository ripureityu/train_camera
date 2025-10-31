import engineio           # リアルタイム通信用
import flask              # Webサーバ用
import waitress           # WSGIサーバ用

app = flask.Flask(__name__)

eio = engineio.Server(
    allow_upgrades=False,
    transports=["polling"],  # WebSocketを使わずpollingのみ
)

# 踏切ごとのセッションID管理: { crossing_id: sid }
sidlist = {}

@eio.on("connect")
def connect(sid, environ):
    print("Connected: ", sid)  # クライアント接続時

@eio.on("disconnect")
def disconnect(sid):
    # 切断された sid に紐づく crossing_id を削除
    keys_to_remove = [k for k, v in sidlist.items() if v == sid]
    for k in keys_to_remove:
        del sidlist[k]
    print("Disconnected:", sid)

@eio.on("message")
def message(sid, msg):
    # crossing-id受信時は踏切IDとセッションIDを紐付け
    try:
        if isinstance(msg, str) and msg.startswith("crossing-id "):
            sp = msg.split()
            if len(sp) >= 2:
                crossing_id = sp[1]
                sidlist[crossing_id] = sid
                print(f"Registered crossing-id {crossing_id} -> sid {sid}")
        else:
            # その他メッセージはログだけにする
            print(f"message from {sid}: {msg}")
    except Exception as e:
        print("message handler error:", e)

@app.route("/vigcamera", methods=["GET"])
def index():
    # 列車側から踏切カメラに撮影リクエスト
    crossing_id = flask.request.args.get("crossing-id","")
    print("vigcamera", crossing_id)
    sid = sidlist.get(crossing_id)
    if not sid:
        return "no session for crossing-id", 404
    # 踏切カメラにリクエスト送信（クライアント側で受信処理を実装すること）
    try:
        eio.send(sid, "picture request")
    except Exception as e:
        print("eio.send error:", e)
        return "send failed", 500
    return "send ok"

picture_data = {}  # crossing-idごとの画像データ保存

@app.route("/picture", methods=["POST"])
def picture():
    # 踏切カメラから画像データ受信
    crossing_id = flask.request.args.get("crossing-id","")
    if not crossing_id:
        return "missing crossing-id", 400
    data = flask.request.get_data()
    if not data:
        return "no data", 400
    picture_data[crossing_id] = data
    print(f"Received picture for {crossing_id}, {len(data)} bytes")
    return "ok"

@app.route("/get_picture", methods=["GET"])
def get_picture():
    # 列車側から画像データ取得
    crossing_id = flask.request.args.get("crossing-id","")
    if not crossing_id:
        return "missing crossing-id", 400
    data = picture_data.get(crossing_id)
    if data is None:
        return "no picture", 404
    # バイト列をそのまま返す（クライアント側が画像として解釈する）
    return flask.Response(data, mimetype="application/octet-stream")

if __name__ == "__main__":
    # engineio.WSGIApp の使い方: (server, app)
    app_with_eio = engineio.WSGIApp(eio, app)
    waitress.serve(
        app_with_eio,
        host="0.0.0.0",
        port=3000,
    )