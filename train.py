import requests
import tkinter as tk

# responce = requests.get("http://localhost:3000/", params={"key1":"value1","key2":"value2"})
# print(responce.status_code)
# print(responce.text)

# GUIのウィンドウを作成
root = tk.Tk()
root.title("Hello Tkinter")
root.geometry("400x300")
label = tk.Label(
    root,
    image=tk.PhotoImage()
)
label.pack()

def aaa():
    print("1秒経過")
    picture_requests = requests.get("http://localhost:3000/vigcamera", params={"crossing-id":"test1"})

    root.after(1000,bbb)
    
def bbb():
    print("1秒経過")
    picture_requests = requests.get("http://localhost:3000/get_picture", params={"crossing-id":"test1"})
    label.config(image=tk.PhotoImage(data=picture_requests.content))
    root.after(1000,aaa)
root.after(1000,aaa)
    
root.mainloop()
