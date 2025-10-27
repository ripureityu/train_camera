import serial
import micropyGPS
from geopy.distance import geodesic

def geopy(train_lat,train_lon,cross_lat,cross_lon):
    distance = geodesic([train_lat,train_lon],[cross_lat,cross_lon]).kilometers
    if distance <= 2.0:
        print("踏切まで2km以内")
    return distance
xxx = geopy(0,0,0,1)
print(xxx)



gps = micropyGPS.MicropyGPS(9, 'dd') # MicroGPSオブジェクトを生成する。
                                     # 引数はタイムゾーンの時差と出力フォーマット
 
def rungps(): # GPSモジュールを読み、GPSオブジェクトを更新する
    s = serial.Serial('/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_u-blox_7_-_GPS_GNSS_Receiver-if00', 9600, timeout=10)
    s.readline() # 最初の1行は中途半端なデーターが読めることがあるので、捨てる
    while True:
        sentence = s.readline().decode('utf-8') # GPSデーターを読み、文字列に変換する
        if sentence[0] != '$': # 先頭が'$'でなければ捨てる
            continue
        for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
            gps.update(x)
        if gps.clean_sentences > 20: # ちゃんとしたデーターがある程度たまったら出力する
            print('緯度経度: %2.8f, %2.8f' % (gps.latitude[0], gps.longitude[0]))
        geopy(0,0,0,0)
rungps()

