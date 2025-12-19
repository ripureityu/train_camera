import requests              # HTTPリクエスト用
import tkinter as tk         # GUI用
import serial                # シリアル通信用
import micropyGPS            # GPSデータ解析用         
from geopy.distance import geodesic  # 距離計算用
from ultralytics.models.yolo import YOLO

import cv2
import numpy as np
import traceback

crossing_list=[
  [36.433884, 140.471628, "test0"],
  [36.344530, 140.28962, "test1"],
  [35.9337819,140.6531255,"ibrk2"],
  [35.9348979,140.6535295,"ibrk3"],
  [35.9360474,140.6537077,"ibrk4"],
  [35.9372999,140.6538089,"ibrk5"],
  [35.9395733,140.6539902,"ibrk6"],
  [35.9578097,140.6551653,"ibrk7"],
  [35.9588946,140.6545967,"ibrk8"],
  [35.8958528,140.6612983,"ibrk9"],
  [36.2139158,139.9741185,"ibrk10"],
  [36.252251,139.9745869,"ibrk11"],
  [36.0093402,139.9824804,"ibrk12"],
  [36.0406432,139.9916338,"ibrk13"],
  [36.0417504,139.9914601,"ibrk14"],
  [35.997257,139.9803657,"ibrk15"],
  [35.9932632,139.9805831,"ibrk16"],
  [35.9995441,139.9802477,"ibrk17"],
  [35.9689469,139.985219,"ibrk18"],
  [35.9178951,140.0416227,"ibrk19"],
  [35.9614988,139.987753,"ibrk20"],
  [36.1503021,139.9707811,"ibrk21"],
  [36.1552207,139.9704221,"ibrk22"],
  [36.1761949,139.9663338,"ibrk23"],
  [36.1773346,139.966062,"ibrk24"],
  [36.0195492,139.9940629,"ibrk25"],
  [36.0204561,139.9950333,"ibrk26"],
  [36.039372,139.9918235,"ibrk27"],
  [36.0486067,139.9904863,"ibrk28"],
  [36.0491118,139.9904093,"ibrk29"],
  [36.0638131,139.9861935,"ibrk30"],
  [36.097324,139.9748002,"ibrk31"],
  [36.0975877,139.974653,"ibrk32"],
  [36.0989187,139.974067,"ibrk33"],
  [36.1044175,139.9740866,"ibrk34"],
  [36.1058103,139.9742008,"ibrk35"],
  [36.1109464,139.9746405,"ibrk36"],
  [36.1258214,139.9715909,"ibrk37"],
  [36.1332603,139.9696929,"ibrk38"],
  [36.2379754,139.9758093,"ibrk39"],
  [36.2410849,139.9755427,"ibrk40"],
  [35.9127227,140.0526661,"ibrk41"],
  [35.9214351,140.1519953,"ibrk42"],
  [35.9203326,140.1544426,"ibrk43"],
  [35.9195965,140.156078,"ibrk44"],
  [35.9142932,140.1680359,"ibrk45"],
  [35.9139515,140.1686935,"ibrk46"],
  [36.3716247,140.5557312,"ibrk47"],
  [36.3709533,140.5567317,"ibrk48"],
  [36.3699498,140.558274,"ibrk49"],
  [36.3692811,140.5592743,"ibrk50"],
  [36.368621,140.5602781,"ibrk51"],
  [36.3644498,140.5674031,"ibrk52"],
  [36.3636005,140.5682991,"ibrk53"],
  [36.3612824,140.5707961,"ibrk54"],
  [36.3601103,140.5720506,"ibrk55"],
  [36.3577499,140.5745524,"ibrk56"],
  [36.3565808,140.5758153,"ibrk57"],
  [36.354253,140.5783235,"ibrk58"],
  [36.3513778,140.5813963,"ibrk59"],
  [36.3444601,140.5895345,"ibrk60"],
  [36.409934,140.4833555,"ibrk61"],
  [36.5114285,140.4314059,"ibrk62"],
  [36.5501857,140.4106058,"ibrk63"],
  [36.5608984,140.3930672,"ibrk64"],
  [36.5831673,140.3750976,"ibrk65"],
  [36.524459,140.5266774,"ibrk66"],
  [36.4746826,140.4960816,"ibrk67"],
  [36.478679,140.4997355,"ibrk68"],
  [36.4875376,140.5031429,"ibrk69"]
]


# GPSオブジェクトを生成（タイムゾーン9、出力フォーマット'dd'）
gps = micropyGPS.MicropyGPS(9, 'dd')
model = YOLO("yolo11n.pt") 


def geopy(train_lat,train_lon,cross_lat,cross_lon):
    distance = geodesic([train_lat,train_lon],[cross_lat,cross_lon]).kilometers
    if distance <= 2.0:
        print("踏切まで2km以内")
    return distance

# --- YOLO 統合関数（改善版） ---
def ai_function_from_bytes(picture_bytes, conf_thres=0.25, imgsz=640):
    """
    バイト列 -> OpenCV デコード -> RGB変換 -> YOLO 推論。
    'person' が見つかれば True を返す。例外発生時は False。
    """
    try:
        nparr = np.frombuffer(picture_bytes, np.uint8)
        img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img_bgr is None:
            print("画像デコード失敗")
            return False
        # BGR -> RGB
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        # Ultralytics に numpy array のリストで渡す（明示的に conf とサイズを指定）
        results = model.predict(source=[img_rgb], imgsz=imgsz, conf=conf_thres, verbose=False)
        if not results:
            return False
        r = results[0]

        # フォールバック: summary() による走査（古い/別実装向け）
        if hasattr(r, "summary"):
            summary = r.summary() or []
            for item in summary:
                if item.get("name") == "person":
                    return True

        return False
    except Exception:
        print("YOLO 推論エラー:")
        traceback.print_exc()
        return False


# GUIウィンドウ作成
root = tk.Tk()
root.title("Hello Tkinter")
root.geometry("1200x1000")
image=tk.PhotoImage()  # 画像表示用
label = tk.Label(
    root,
    image=image,
    height=600,
    width=800,
)
label.pack()

s = serial.Serial('/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_u-blox_7_-_GPS_GNSS_Receiver-if00', 9600, timeout=10)
s.readline() # 最初の1行は中途半端なデーターが読めることがあるので、捨てる


def aaa():
    sentence = s.readline().decode('utf-8') # GPSデーターを読み、文字列に変換する
    if not sentence or sentence[0] != '$': # 先頭が'$'でなければ捨てる
        root.after(10,aaa)
        return
    for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
        gps.update(x)
    if gps.clean_sentences > 20: # ちゃんとしたデーターがある程度たまったら出力する
        print('緯度経度: %2.8f, %2.8f' % (gps.latitude[0], gps.longitude[0]))
        
        crossing_list.sort(key=lambda x: geopy(gps.latitude[0], gps.longitude[0],x[0],x[1]))
        nearest_distance = geopy(gps.latitude[0], gps.longitude[0], crossing_list[0][0], crossing_list[0][1])
        requests.get("http://localhost:3000/vigcamera", params={"crossing-id":"test1"})
        root.after(1000,bbb)
    root.after(1000,aaa)

def bbb():
    # 1秒ごとに画像データを取得し表示
    try:
        print("1秒経過")
        picture_requests = requests.get("http://localhost:3000/get_picture", params={"crossing-id":"test1"}, timeout=5)
        data = picture_requests.content
        print(data)
        print(type(data))  # データ型確認
        print(str(data[:10],"utf-8","ignore")) # 先頭10バイトを表示（デバッグ）

        # Tkinter の PhotoImage は PNG を期待する場合があるため例外を捕まえる
        try:
            image.config(
                data=data,
                format="png"
            )
        except Exception:
            # 表示に失敗しても検出は行う
            pass

        # ここで受信した画像データに対して人物検出を行う
        detected = ai_function_from_bytes(data)
        print("person detected:", detected)
        # 必要に応じて検出時の処理（通知など）を追加してください
    except Exception:
        print("画像取得/処理エラー:")
        traceback.print_exc()
    finally:
        # 次回も1秒後に画像取得（ループを維持）
        root.after(1000, bbb)



root.after(1000,aaa)  # 最初の処理を1秒後に開始
root.mainloop()       # GUIイベントループ開始