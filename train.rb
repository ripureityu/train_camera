require 'tk'
require 'net/http'
require 'uri'

root = TkRoot.new { title "Train Camera"; geometry "400x300" }
image = TkPhotoImage.new
label = TkLabel.new(root) { image image; height 600; width 800 }.pack

def aaa
  puts "1秒経過"
  uri = URI("http://localhost:3000/vigcamera?crossing-id=test1")
  Net::HTTP.get(uri)
  Tk.after(1000) { bbb }
end

def bbb
  puts "1秒経過"
  uri = URI("http://localhost:3000/get_picture?crossing-id=test1")
  res = Net::HTTP.get(uri)
  # TkPhotoImageでバイナリ画像表示は難しいため省略
  Tk.after(1000) { aaa }
end

Tk.after(1000) { aaa }
Tk.mainloop