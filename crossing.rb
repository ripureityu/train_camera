require 'faye/websocket'    # WebSocket通信のためのライブラリ
require 'eventmachine'      # 非同期イベント処理ライブラリ
require 'net/http'          # HTTP通信のためのライブラリ
require 'uri'               # URI操作用ライブラリ

EM.run do
  # WebSocketクライアントを作成し、サーバに接続
  ws = Faye::WebSocket::Client.new('ws://localhost:3000/ws')

  # WebSocket接続が確立したときの処理
  ws.on :open do |event|
    ws.send('crossing-id test1')   # crossing-idをサーバに送信して登録
    puts "WebSocket connected"     # 接続完了メッセージ表示
  end

  ws.on :error do  |event|
    p event
    p event.http
    p event.message
    puts "Error: #{event.message}"  # エラーメッセージ表示
  end


  # サーバからメッセージを受信したときの処理
  ws.on :message do |event|
    puts "message: #{event.data}"  # 受信したメッセージを表示
    if event.data == 'picture request'  # サーバから撮影リクエストが来た場合
      buf = File.binread('image.jpg')   # image.jpgファイルをバイナリで読み込む
      uri = URI('http://localhost:3000/picture?crossing-id=test1') # crossing-idをURLに含める
      headers = { 'Content-Type' => 'application/octet-stream' }   # バイナリ送信時はContent-Typeを指定

      Net::HTTP.start(uri.host, uri.port) do |http|

        req = Net::HTTP::Post.new(uri, headers)
        req.body = buf
        res = http.request(req)
        puts res.body
      end

      puts "画像データを送信しました"     # 送信完了メッセージ表示
    end
  end

  # WebSocket接続が切断されたときの処理
  ws.on :close do |event|
    puts "WebSocket closed"         # 切断メッセージ表示
    EM.stop                         # EventMachineのループを停止
  end

end
