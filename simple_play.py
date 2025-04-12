# simple_play.py
import os
import mss
import mss.tools
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
import time
from pynput import keyboard
from pynput.keyboard import Key, Controller

# Khu vực game - điều chỉnh theo màn hình của bạn
GAME = {"top": 200, "left": 250, "width": 600, "height": 500}

# Tạo bộ điều khiển bàn phím
keyboard_controller = Controller()

# Tải mô hình đã huấn luyện
print("Đang tải mô hình...")
model = tf.keras.models.load_model('models/Sequential.keras')

print("Bắt đầu chơi game tự động sau 5 giây...")
print("Nhấn ESC để thoát.")
time.sleep(5)

# Các lựa chọn hành động
actions = ['left', 'right', 'up', 'down', 'noop']
last_action = None
last_time = time.time()

# Tạo biến để kiểm soát thoát
stop_game = False

def on_press(key):
    global stop_game
    if key == keyboard.Key.esc:
        stop_game = True
        return False

listener = keyboard.Listener(on_press=on_press)
listener.start()

# Hàm thực hiện hành động
def take_action(action):
    if action == 'noop':
        return
        
    key_map = {
        'left': Key.left,
        'right': Key.right,
        'up': Key.up,
        'down': Key.down
    }
    
    keyboard_controller.press(key_map[action])
    time.sleep(0.05)
    keyboard_controller.release(key_map[action])

# Vòng lặp chính
with mss.mss() as sct:
    while not stop_game:
        # Chụp màn hình
        img_capture = sct.grab(GAME)
        
        # Chuyển đổi hình ảnh
        img = Image.frombytes("RGB", img_capture.size, img_capture.bgra, "raw", "BGRX")
        img = np.array(img)
        img = cv2.resize(img, (96, 96))
        img = np.expand_dims(img, 0)  # Tạo batch kích thước 1
        
        # Dự đoán hành động
        predictions = model.predict(img, verbose=0)  # Tắt thông báo dự đoán
        action_index = np.argmax(predictions[0])
        action = actions[action_index]
        confidence = float(predictions[0][action_index])
        
        # Thực hiện hành động nếu khác với hành động trước đó
        if action != last_action and confidence > 0.3:  # Chỉ thực hiện khi độ tin cậy > 30%
            take_action(action)
            print(f"Hành động: {action} (độ tin cậy: {confidence:.2f})")
            last_action = action
        
        # Tính FPS
        current_time = time.time()
        fps = 1 / (current_time - last_time)
        last_time = current_time
        
        # Hiển thị FPS mỗi 2 giây
        if int(current_time) % 2 == 0:
            print(f"FPS: {fps:.1f}")
        
        # Chờ một chút để giảm tải CPU
        time.sleep(0.05)

print("Đã dừng chơi game!")