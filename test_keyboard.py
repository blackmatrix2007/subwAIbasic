import time
from pynput.keyboard import Key, Controller
import subprocess

def test_keyboard_pynput():
    """Kiểm tra phím với thư viện pynput"""
    print("Kiểm tra pynput keyboard trong 3 giây...")
    time.sleep(3)
    print("Bắt đầu nhấn phím...")
    
    keyboard = Controller()
    
    # Test các phím chữ cái
    for char in "HELLO WORLD":
        keyboard.press(char)
        keyboard.release(char)
        time.sleep(0.2)
    
    print("Hoàn thành test phím chữ cái")
    time.sleep(1)
    
    # Test các phím mũi tên
    arrow_keys = [Key.left, Key.right, Key.up, Key.down]
    for key in arrow_keys:
        print(f"Nhấn phím {key}")
        keyboard.press(key)
        time.sleep(0.2)
        keyboard.release(key)
        time.sleep(0.5)
    
    print("Hoàn thành test phím mũi tên với pynput")

def test_keyboard_applescript():
    """Kiểm tra phím với AppleScript"""
    print("Kiểm tra AppleScript keyboard trong 3 giây...")
    time.sleep(3)
    print("Bắt đầu nhấn phím...")
    
    # Test các phím chữ cái
    for char in "HELLO WORLD":
        script = f'''
        tell application "System Events"
            keystroke "{char}"
        end tell
        '''
        subprocess.run(['osascript', '-e', script])
        time.sleep(0.2)
    
    print("Hoàn thành test phím chữ cái với AppleScript")
    time.sleep(1)
    
    # Test các phím mũi tên
    key_codes = {
        'left': '123',
        'right': '124',
        'up': '126',
        'down': '125'
    }
    
    for key, code in key_codes.items():
        print(f"Nhấn phím {key}")
        script = f'''
        tell application "System Events"
            key code {code}
        end tell
        '''
        subprocess.run(['osascript', '-e', script])
        time.sleep(0.5)
    
    print("Hoàn thành test phím mũi tên với AppleScript")

def test_keyboard_pyautogui():
    """Kiểm tra phím với PyAutoGUI"""
    try:
        import pyautogui
        print("Kiểm tra PyAutoGUI keyboard trong 3 giây...")
        time.sleep(3)
        print("Bắt đầu nhấn phím...")
        
        # Test các phím chữ cái
        pyautogui.write("HELLO WORLD", interval=0.2)
        
        print("Hoàn thành test phím chữ cái với PyAutoGUI")
        time.sleep(1)
        
        # Test các phím mũi tên
        arrow_keys = ['left', 'right', 'up', 'down']
        for key in arrow_keys:
            print(f"Nhấn phím {key}")
            pyautogui.press(key)
            time.sleep(0.5)
        
        print("Hoàn thành test phím mũi tên với PyAutoGUI")
    except ImportError:
        print("PyAutoGUI không được cài đặt. Bỏ qua test này.")

if __name__ == "__main__":
    print("HƯỚNG DẪN: Mở một trình soạn thảo văn bản hoặc website bàn phím ảo để kiểm tra")
    print("1 - Test với pynput")
    print("2 - Test với AppleScript")
    print("3 - Test với PyAutoGUI (cần cài thêm thư viện)")
    print("0 - Test tất cả")
    
    choice = input("Lựa chọn của bạn (0-3): ")
    
    if choice == "1" or choice == "0":
        test_keyboard_pynput()
    
    if choice == "2" or choice == "0":
        test_keyboard_applescript()
    
    if choice == "3" or choice == "0":
        test_keyboard_pyautogui()