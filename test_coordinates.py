import mss
import mss.tools
import cv2
import numpy as np
import time
import os

# Điều chỉnh các tọa độ này cho đến khi chúng chụp đúng khu vực game
GAME = {"top": 200, "left": 250, "width": 600, "height": 500} 

# Đảm bảo thư mục tồn tại
os.makedirs("debug", exist_ok=True)

with mss.mss() as sct:
    print("Chụp màn hình sau 3 giây...")
    time.sleep(3)
    img = sct.grab(GAME)
    mss.tools.to_png(img.rgb, img.size, output="debug/game_capture.png")
    print(f"Đã lưu ảnh chụp màn hình vào debug/game_capture.png")
    
    # Chuyển đổi sang định dạng OpenCV
    cv_img = np.array(img)
    # Chuyển từ BGRA sang BGR
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGRA2BGR)
    
    # Hiển thị để kiểm tra
    cv2.imshow("Captured Game Area", cv_img)
    print("Nhấn phím bất kỳ để đóng cửa sổ xem trước")
    cv2.waitKey(0)
    cv2.destroyAllWindows()