import engineio
import flask
import waitress

# import logging
# logger = logging.getLogger('waitress')
# logger.setLevel(logging.DEBUG)

app = flask.Flask(__name__)

eio = engineio.Server(
    # logger=True,
    allow_upgrades=False,
    transports=["polling"],
)

sidlist = []

@eio.on("connect")
def connect(sid, environ):
    sidlist.append(sid)
    print("Connected: ", sid)

@eio.on("disconnect")
def disconnect(sid):
    sidlist.append(sid)
    print("Disconnected: ", sid)

@app.route("/")
def index():
    for sid in sidlist:
        eio.send(sid, "aaa")
        print("send sid:", sid, ", data: aaa")
    return ""

@eio.on("message")
def on_message(sid, data):
    # バイナリデータの場合、画像として保存
    if isinstance(data, bytes):
        with open("received_image.jpg", "w") as f:
            f.write(str(data))
        print("画像を保存しました: received_image.jpg")
    else:
        print("message from", sid, ":", data)

if __name__ == "__main__":
    waitressapp = engineio.WSGIApp(eio, wsgi_app=app)
    waitress.serve(
        waitressapp,
        host="0.0.0.0",
        port=3000,
    )
