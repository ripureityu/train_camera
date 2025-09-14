import cv2

# カメラを開く
cap = cv2.VideoCapture(0)

# 画像をキャプチャする
ret, frame = cap.read()

# 画像を保存する
cv2.imwrite("image.jpg", frame)

# カメラを閉じる
cap.release()