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

eio.wait()
