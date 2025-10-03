require 'faye/websocket'
require 'eventmachine'
require 'net/http'
require 'uri'

EM.run do
  ws = Faye::WebSocket::Client.new('ws://localhost:3000/ws')

  ws.on :open do |event|
    ws.send('crossing-id test1')
    puts "WebSocket connected"
  end

  ws.on :message do |event|
    puts "message: #{event.data}"
    if event.data == 'picture request'
      buf = File.binread('image.jpg')
      uri = URI('http://localhost:3000/picture?crossing-id=test1')
      Net::HTTP.post(uri, buf)
      puts "画像データを送信しました"
    end
  end

  ws.on :close do |event|
    puts "WebSocket closed"
    EM.stop
  end
end
