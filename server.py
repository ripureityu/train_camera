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

sidlist = {}#踏切

@eio.on("connect")
def connect(sid, environ):
    print("Connected: ", sid)

@eio.on("disconnect")
def disconnect(sid):
    sidlist.append(sid)
    print("Disconnected:", sid)

@eio.on("message")
def message(sid, msg: str):
    if msg.startswith("crossing-id "):
        sp = msg.split()
        crossing_id = sp[1]
        sidlist[crossing_id] = sid #crossing_id:キー,sid:値としてdictに保存 
    elif msg == "crossing_send":
        with open("receive.jpg", "wb") as f:
            img = eio.receive(sid)
            pictute =  f.write(msg)
            eio.send()    
        
@app.route("/vigcamera", methods=["GET"])
def index():
    crossing_id = flask.request.args.get("crossing-id","")
    sid  = sidlist[crossing_id]#sidlistをsidに代入
    eio.send(sid,"picture request")#踏切にメッセージ送信
    eio.send(sid, "stop picture")
    return "send ok"

# ?v=GvpmzUUCTZk&t=2s
# v GvpmzUUCTZk t 2s

  
if __name__ == "__main__":
    waitressapp = engineio.WSGIApp(eio, wsgi_app=app)
    waitress.serve(
        waitressapp,
        host="0.0.0.0",
        port=3000,
    )
