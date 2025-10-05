require 'tk'

TEMP_FILE_NAME = "temp.png"
root = TkRoot.new { title "Hello Tkinter"; geometry "400x300" }

bbb = TkPhotoImage.new(:width=>800, :height=>600)
data = File.binread("aaa.png")
File.binwrite(TEMP_FILE_NAME, data)
bbb.read(TEMP_FILE_NAME, {"format": "png"})
label = TkLabel.new { image bbb; width 800; height 600}.pack
Tk.mainloop
