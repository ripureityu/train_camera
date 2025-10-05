import requests
import tkinter as tk
import serial
import micropyGPS
import threading
from geopy.distance import geodesic


gps = micropyGPS.MicropyGPS(9, 'dd') # MicroGPSオブジェクトを生成する。
                                     # 引数はタイムゾーンの時差と出力フォーマット
 
def run_gps(): # GPSモジュールを読み、GPSオブジェクトを更新する
    s = serial.Serial('/dev/tty.usbmodem14301', 9600, timeout=10)
    s.readline() # 最初の1行は中途半端なデーターが読めることがあるので、捨てる
    while True:
        sentence = s.readline().decode('utf-8') # GPSデーターを読み、文字列に変換する
        if sentence[0] != '$': # 先頭が'$'でなければ捨てる
            continue
        for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
            gps.update(x)
        
 
gpsthread = threading.Thread(target=run_gps, args=()) # 上の関数を実行するスレッドを生成
gpsthread.daemon = True
gpsthread.start() # スレッドを起動
 
def print_gps():
    if gps.clean_sentences > 20: # ちゃんとしたデーターがある程度たまったら出力する
        h = gps.timestamp[0] if gps.timestamp[0]  else gps.timestamp[0] - 24
        print('%2d:%02d:%04.1f' % (h, gps.timestamp[1], gps.timestamp[2]))
        print('緯度経度: %2.8f, %2.8f')
        print('%2.8f, %2.8f' % (gps.latitude[0], gps.longitude[0]))
        print('海抜: %f' % gps.altitude)
        #参考記事だとここに測位利用衛星を出力する記述が入る
        print('衛星番号: (仰角, 方位角, SN比)')
        for k, v in gps.satellite_data.items():
            print('%d: %s' % (k, v))

def geopy(distance):
    cross_list = [36.370856,140.476135]
    train_list=['%2.8f','%2.8f']
    distance = geodesic([cross_list[0],cross_list[1]],[train_list[0],train_list[1]]).kilometers
    if distance <= 2.0:
        aaa()
        print("踏切まで2km以内")
    return distance


# GUIのウィンドウを作成
root = tk.Tk()
root.title("Hello Tkinter")
root.geometry("400x300")
image=tk.PhotoImage()
label = tk.Label(
    root,
    image=image,
    height=600,
    width=800,
)
label.pack()

def aaa():
    print("1秒経過")
    requests.get("http://localhost:3000/vigcamera", params={"crossing-id":"test1"})

    root.after(1000,bbb)
    
def bbb():
    print("1秒経過")
    picture_requests = requests.get("http://localhost:3000/get_picture", params={"crossing-id":"test1"})
    data = picture_requests.content
    print(type(picture_requests.content))
    print(str(data[:10],"utf-8","ignore"))
    image.config(
        data=picture_requests.content,                 
        format="png",
    )
    root.after(1000,aaa)
root.after(1000,aaa)
    
root.mainloop()

 
