# OpenCV を使うためのモジュールを読み込む
import cv2
# Ultralytics YOLO モデルクラスを読み込む
from ultralytics.models.yolo import YOLO
# NumPy を配列操作用に読み込む
import numpy as np

# YOLO モデルをファイルから読み込み（モデルファイル名を指定）
model = YOLO("yolo11n.pt") 


# バイト列を受け取ってクラス検出を行う関数を定義
def cls(data: bytes):#bytes
    # 受信したバイト列を NumPy の uint8 配列に変換
    nparray = np.frombuffer(data, np.uint8)
    # NumPy 配列を OpenCV で画像にデコード（BGR 形式）
    img = cv2.imdecode(nparray, cv2.IMREAD_COLOR)
    # デコードに失敗した場合はエラーを返す
    if img is None:
        return "error"

    # デコードした画像を YOLO モデルで推論
    results = model.predict(img)
    # 推論結果の最初のフレームのボックス情報を取得
    boxes = results[0].boxes
    # ボックス情報が無ければエラーを返す
    if boxes is None:
        return "error"

    # ボックスのクラスID列を Python のリストに変換
    boxes_cls = boxes.cls.tolist()
    if 0.0 in boxes_cls:
        return 'person'
    elif 2.0 in boxes_cls:
        return 'car'
    # クラスIDリストを出力（デバッグ用）
    print(boxes_cls)
    return 'detected'

# このファイルが直接実行されたときの処理（今回は何もしない）
if __name__ == '__main__':
    with open("Untitled.png","rb") as f:
        data = f.read()
        word=cls(data)
        assert data == "person"
    with open("car.png","rb") as f:
        data = f.read()
        word=cls(data)
        assert data == "car"
    with open("urs.png","rb") as f:
        data = f.read()
        word=cls(data)
        assert data == "detected"