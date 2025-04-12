# simple_gather.py
import mss
import mss.tools
import time
import cv2
import numpy as np
import os
from pynput import keyboard

# Tạo thư mục
os.makedirs("images/training/left", exist_ok=True)
os.makedirs("images/training/right", exist_ok=True)
os.makedirs("images/training/up", exist_ok=True)
os.makedirs("images/training/down", exist_ok=True)
os.makedirs("images/training/noop", exist_ok=True)

# Tọa độ khu vực game
GAME = {"top": 200, "left": 250, "width": 600, "height": 500}

# Theo dõi phím
pressed_keys = set()

def on_press(key):
    global pressed_keys
    try:
        pressed_keys.add(key.char)
    except AttributeError:
        pressed_keys.add(str(key))
        
def on_release(key):
    global pressed_keys
    try:
        pressed_keys.discard(key.char)
    except AttributeError:
        pressed_keys.discard(str(key))
    
    # Thoát khi nhấn ESC
    if key == keyboard.Key.esc:
        return False

# Thiết lập bộ lắng nghe phím
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

counter = {
    "left": 0,
    "right": 0,
    "up": 0,
    "down": 0,
    "noop": 0
}

print("Bắt đầu thu thập dữ liệu. Nhấn ESC để thoát.")
print("Sử dụng các phím mũi tên để điều khiển.")
print("Bắt đầu sau 3 giây...")
time.sleep(3)

with mss.mss() as sct:
    while True:
        # Chụp màn hình
        img = sct.grab(GAME)
        
        # Xác định hành động
        action = "noop"
        if 'left' in pressed_keys or 'Key.left' in pressed_keys:
            action = "left"
        elif 'right' in pressed_keys or 'Key.right' in pressed_keys:
            action = "right"
        elif 'up' in pressed_keys or 'Key.up' in pressed_keys:
            action = "up"
        elif 'down' in pressed_keys or 'Key.down' in pressed_keys:
            action = "down"
            
        # Lưu hình ảnh với tỉ lệ 1:20 (để giảm số lượng noop)
        if action != "noop" or np.random.random() < 0.05:
            counter[action] += 1
            filename = f"images/training/{action}/{counter[action]}.png"
            mss.tools.to_png(img.rgb, img.size, output=filename)
            print(f"Đã lưu {filename} - {action}")
            
        # Hiển thị trạng thái
        if counter["left"] % 10 == 0 and counter["left"] > 0:
            print(f"Trạng thái: Left: {counter['left']}, Right: {counter['right']}, Up: {counter['up']}, Down: {counter['down']}, Noop: {counter['noop']}")
            
        # Thoát nếu ESC được nhấn
        if not listener.is_alive():
            break
            
        time.sleep(0.1)  # Chờ 0.1 giây giữa các lần chụp

print("Đã hoàn tất thu thập dữ liệu:")
print(f"Left: {counter['left']}, Right: {counter['right']}, Up: {counter['up']}, Down: {counter['down']}, Noop: {counter['noop']}")