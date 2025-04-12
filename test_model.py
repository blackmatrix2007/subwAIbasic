# test_model.py
import os
import numpy as np
import cv2
import tensorflow as tf
import random
from PIL import Image

# Tải mô hình
model = tf.keras.models.load_model('models/Sequential')

# Các nhãn hành động
actions = ['left', 'right', 'up', 'down', 'noop']

# Chọn ngẫu nhiên một số hình ảnh từ tập dữ liệu để kiểm tra
test_images = []
true_labels = []

for i, action in enumerate(actions):
    folder_path = os.path.join('images/training', action)
    if not os.path.exists(folder_path):
        continue
        
    image_files = os.listdir(folder_path)
    selected_files = random.sample(image_files, min(10, len(image_files)))
    
    for image_file in selected_files:
        img_path = os.path.join(folder_path, image_file)
        img = cv2.imread(img_path)
        if img is None:
            continue
            
        img = cv2.resize(img, (96, 96))
        test_images.append(img)
        true_labels.append(i)

# Chuyển đổi thành mảng numpy
test_images = np.array(test_images)
true_labels = np.array(true_labels)

# Dự đoán với mô hình
predictions = model.predict(test_images)
predicted_labels = np.argmax(predictions, axis=1)

# Tính độ chính xác
accuracy = np.mean(predicted_labels == true_labels)
print(f"Độ chính xác trên tập kiểm tra: {accuracy:.4f}")

# Hiển thị một số ví dụ
for i in range(min(5, len(test_images))):
    img = test_images[i]
    true_action = actions[true_labels[i]]
    predicted_action = actions[predicted_labels[i]]
    confidence = predictions[i][predicted_labels[i]]
    
    print(f"Hình ảnh {i+1}:")
    print(f"  Nhãn thực: {true_action}")
    print(f"  Dự đoán: {predicted_action} (độ tin cậy: {confidence:.4f})")
    
    # Hiển thị hình ảnh
    cv2.imshow(f"Image {i+1}: True={true_action}, Pred={predicted_action}", img)
    cv2.waitKey(0)
    
cv2.destroyAllWindows()