from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2
import numpy as np
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def process_image(image):
    # グレースケール変換
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
    return processed_image

@app.route('/')
def index():
    return render_template('index_gray.html')

@socketio.on('process_image')
def handle_image(data):
    # データがbase64形式かどうか確認し、必要であれば分割
    if ',' in data:
        encoded_data = data.split(',')[1]
    else:
        encoded_data = data  # 万が一のためのフォールバック
    
    # base64デコード
    try:
        np_data = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    except Exception as e:
        return
    
    # OpenCVでデコード
    if np_data.size == 0:
        return
    
    img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
    if img is None:
        return
    
    # 画像を処理
    processed_img = process_image(img)
    
    # 画像をbase64エンコード
    _, buffer = cv2.imencode('.jpg', processed_img)
    processed_img_base64 = base64.b64encode(buffer).decode('utf-8')
    
    # クライアントに処理済み画像を送信
    emit('response_image', 'data:image/jpeg;base64,' + processed_img_base64)

if __name__ == '__main__':
    socketio.run(app, debug=True)
