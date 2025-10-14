import requests              # HTTPリクエスト用
import tkinter as tk         # GUI用
import serial                # シリアル通信用
import micropyGPS            # GPSデータ解析用
import threading             # スレッド処理用
from geopy.distance import geodesic  # 距離計算用

# GPSオブジェクトを生成（タイムゾーン9、出力フォーマット'dd'）
gps = micropyGPS.MicropyGPS(9, 'dd')

def run_gps():
    # シリアルポートを開く（GPS受信器からデータ取得）
    s = serial.Serial('/dev/tty.usbmodem14301', 9600, timeout=10)
    s.readline()  # 最初の1行は捨てる（不完全な場合があるため）
    while True:
        sentence = s.readline().decode('utf-8')  # 1行受信し文字列化
        if sentence[0] != '$':  # NMEAデータでなければスキップ
            continue
        for x in sentence:      # 1文字ずつGPSオブジェクトに渡して解析
            gps.update(x)

# GPS受信スレッドを起動
gpsthread = threading.Thread(target=run_gps, args=())
gpsthread.daemon = True
gpsthread.start()

def print_gps():
    # ある程度データが溜まったら表示
    if gps.clean_sentences > 20:
        h = gps.timestamp[0] if gps.timestamp[0] else gps.timestamp[0] - 24
        print('%2d:%02d:%04.1f' % (h, gps.timestamp[1], gps.timestamp[2]))
        print('%2.8f, %2.8f' % (gps.latitude[0], gps.longitude[0]))
        print('衛星番号: (仰角, 方位角, SN比)')
        for k, v in gps.satellite_data.items():
            print('%d: %s' % (k, v))

def geopy(distance):
    # 踏切座標と列車座標で距離計算
    cross_list = [36.370856,140.476135]
    train_list=['%2.8f'% (gps.latitude[0], gps.longitude[0]),'%2.8f'% (gps.latitude[0], gps.longitude[0])]  # 本来はgps.latitude[0], gps.longitude[0]を使う
    distance = geodesic([cross_list[0],cross_list[1]],[train_list[0],train_list[1]]).kilometers
    if distance <= 2.0:
        aaa()
        print("踏切まで2km以内")
    return distance

# GUIウィンドウ作成
root = tk.Tk()
root.title("Hello Tkinter")
root.geometry("400x300")
image=tk.PhotoImage()  # 画像表示用
label = tk.Label(
    root,
    image=image,
    height=600,
    width=800,
)
label.pack()

def aaa():
    # 1秒ごとに踏切カメラに撮影リクエストを送信
    print("1秒経過")
    requests.get("http://localhost:3000/vigcamera", params={"crossing-id":"test1"})
    root.after(1000,bbb)

def bbb():
    # 1秒ごとに画像データを取得し表示
    print("1秒経過")
    picture_requests = requests.get("http://localhost:3000/get_picture", params={"crossing-id":"test1"})
    data = picture_requests.content
    print(type(picture_requests.content))  # データ型確認
    print(str(data[:10],"utf-8","ignore")) # 先頭10バイトを表示
    image.config(
        data=picture_requests.content,     # 画像データを表示（PNG形式）
        format="png",
    )
    root.after(1000,aaa)

root.after(1000,aaa)  # 最初の処理を1秒後に開始
root.mainloop()       # GUIイベントループ開始