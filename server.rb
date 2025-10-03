require 'sinatra'           # Sinatra: 軽量Webアプリケーションフレームワーク
require 'faye/websocket'    # faye-websocket: WebSocketサーバ/クライアント用ライブラリ
require 'thread'            # スレッド制御用（今回は未使用）
require 'json'              # JSONデータ処理用（今回は未使用）

#set :server, 'thin'         # サーバにthinを指定（WebSocket対応のため）
set :bind, '0.0.0.0'        # 全てのIPアドレスからの接続を許可
set :port, 3000    # ポート番号を3000に設定

connections = {}            # 踏切ごとのWebSocket接続を管理するハッシュ
picture_data = {}           # crossing-idごとの画像データを保存するハッシュ

# 列車側から踏切カメラに撮影リクエストを送るエンドポイント
get '/vigcamera' do
  crossing_id = params['crossing-id']         # crossing-idを取得
  ws = connections[crossing_id]               # 対応するWebSocket接続を取得
  if ws
    ws.send('picture request')                # 踏切カメラに撮影リクエストを送信
    "send ok"                                # 正常時のレスポンス
  else
    "no crossing"                            # 踏切が未接続の場合のレスポンス
  end
end

# 踏切カメラから画像データを受け取るエンドポイント
post '/picture' do
  crossing_id = params['crossing-id']         # crossing-idを取得
  picture_data[crossing_id] = request.body.read # 画像データを保存
  "ok"                                       # 正常時のレスポンス
end

# 列車側から画像データを取得するエンドポイント
get '/get_picture' do
  crossing_id = params['crossing-id']         # crossing-idを取得
  content_type 'image/png'                    # レスポンスのContent-Typeを画像に設定
  picture_data[crossing_id] || ""             # 画像データを返す（なければ空文字）
end

# 踏切カメラ用WebSocket接続エンドポイント
get '/ws' do
  if Faye::WebSocket.websocket?(env)          # WebSocketリクエストか判定
    ws = Faye::WebSocket.new(env)             # WebSocketオブジェクト生成
    crossing_id = nil                         # crossing-id初期化

    # クライアントからメッセージ受信時の処理
    ws.on :message do |event|
      if event.data.start_with?('crossing-id ')
        crossing_id = event.data.split(' ')[1] # crossig-idを抽出
        connections[crossing_id] = ws          # 接続を保存
      end
    end

    # クライアント切断時の処理
    ws.on :close do |event|
      connections.delete(crossing_id) if crossing_id # 接続情報削除
      ws = nil
    end

    ws.rack_response                      # WebSocket用のレスポンスを返す
  else
    status 400                            # WebSocket以外はエラー
    body 'WebSocket only'
  end
end
