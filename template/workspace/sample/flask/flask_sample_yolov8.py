from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2
import numpy as np
import base64
import time

from ultralytics import YOLO
from logging import getLogger

logger = getLogger('ultralytics')
logger.disabled = True

model_bbox = YOLO("yolov8n.pt")
model_bbox(np.zeros((512, 512, 3), dtype=np.uint8))[0]

model_seg = YOLO("yolov8n-seg.pt")
model_seg(np.zeros((512, 512, 3), dtype=np.uint8))[0]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


# 画像処理
def process_image1(image):
    # 処理開始時間の記録
    start_time = time.time()
    
    # モデルによる画像処理
    processed_image = model_bbox(image, conf=0.60)[0].plot()
    
    # 処理時間の計測
    processing_time = time.time() - start_time
    
    # FPSを計算
    fps = 1 / processing_time if processing_time > 0 else 0
    
    # FPSを画像に描画
    cv2.putText(processed_image, f'FPS: {fps:.2f}', (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return processed_image

# 画像処理
def process_image2(image):
    # 処理開始時間の記録
    start_time = time.time()
    
    # モデルによる画像処理
    processed_image = model_seg(image, conf=0.60)[0].plot()
    
    # 処理時間の計測
    processing_time = time.time() - start_time
    
    # FPSを計算
    fps = 1 / processing_time if processing_time > 0 else 0
    
    # FPSを画像に描画
    cv2.putText(processed_image, f'FPS: {fps:.2f}', (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return processed_image

@app.route('/')
def index():
    return render_template('index_yolo.html')

@socketio.on('process_image1')
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
    processed_img = process_image1(img)
    
    # 画像をbase64エンコード
    _, buffer = cv2.imencode('.jpg', processed_img)
    processed_img_base64 = base64.b64encode(buffer).decode('utf-8')
    
    # クライアントに処理済み画像を送信
    emit('response_image1', 'data:image/jpeg;base64,' + processed_img_base64)


@socketio.on('process_image2')
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
    processed_img = process_image2(img)
    
    # 画像をbase64エンコード
    _, buffer = cv2.imencode('.jpg', processed_img)
    processed_img_base64 = base64.b64encode(buffer).decode('utf-8')
    
    # クライアントに処理済み画像を送信
    emit('response_image2', 'data:image/jpeg;base64,' + processed_img_base64)

if __name__ == '__main__':
    socketio.run(app, debug=True)
