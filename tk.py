import tkinter as tk         # GUI用




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