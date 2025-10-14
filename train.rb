require 'tk'
require 'net/http'
require 'uri'

# require 'serialport'
# https://rubydoc.info/gems/serialport/SerialPort

root = TkRoot.new { title "Train Camera"; geometry "400x300" }
images = TkPhotoImage.new
label = TkLabel.new(root) { image images; width 800; height 600}.pack

#sp = SerialPort.new('/dev/tty.usbmodem14201', 115200, 8, 1, 0)


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
  File.binwrite(TEMP_FILE_NAME, res.body)
  images.read(TEMP_FILE_NAME, {"format": "png"})
  Tk.after(1000) { aaa }
end



# def put(data, *opts)


Tk.after(1000) { aaa }
Tk.mainloop

