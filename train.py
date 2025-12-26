import tkinter as tk         # GUI用
import yolo11
import requests               # HTTPリクエスト用



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

def bbb():
    picture_requests = requests.get("http://localhost:3000/get_picture", params={"crossing-id":"test1"}, timeout=5)
    data = picture_requests.content
    image.config(data=data, format="png")
    word = yolo11.cls(data)
    return word
bbb()

if __name__ == '__main__':
    root.mainloop()