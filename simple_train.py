# simple_train.py
import os
import numpy as np
import cv2
import tensorflow as tf
from sklearn.model_selection import train_test_split

# Thông số
IMG_WIDTH = 96
IMG_HEIGHT = 96
NUM_CATEGORIES = 5
EPOCHS = 20
TEST_SIZE = 0.3

def load_data():
    # Tải dữ liệu từ thư mục training
    images = []
    labels = []
    actions = ['left', 'right', 'up', 'down', 'noop']
    
    for i, action in enumerate(actions):
        folder_path = os.path.join('images/training', action)
        if not os.path.exists(folder_path):
            print(f"Thư mục {folder_path} không tồn tại!")
            continue
            
        for image_file in os.listdir(folder_path):
            if not image_file.endswith('.png'):
                continue
                
            # Đọc và thay đổi kích thước hình ảnh
            img_path = os.path.join(folder_path, image_file)
            img = cv2.imread(img_path)
            if img is None:
                print(f"Không thể đọc hình ảnh: {img_path}")
                continue
                
            img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
            images.append(img)
            labels.append(i)
    
    return np.array(images), np.array(labels)

def get_model():
    # Định nghĩa mô hình CNN
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Conv2D(16, (3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])
    
    # Biên dịch mô hình
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    
    return model

# Tạo thư mục lưu trữ mô hình
os.makedirs('models/Sequential', exist_ok=True)

# Tải dữ liệu
print("Đang tải dữ liệu...")
images, labels = load_data()
print(f"Đã tải {len(images)} hình ảnh với nhãn phân phối: {np.bincount(labels)}")

# Chuyển đổi nhãn sang one-hot encoding
labels = tf.keras.utils.to_categorical(labels)

# Chia dữ liệu thành tập huấn luyện và tập kiểm thử
x_train, x_test, y_train, y_test = train_test_split(images, labels, test_size=TEST_SIZE)

# Tạo và huấn luyện mô hình
print("Bắt đầu huấn luyện mô hình...")
model = get_model()
model.fit(x_train, y_train, epochs=EPOCHS, validation_data=(x_test, y_test))

# Đánh giá mô hình
print("Đánh giá mô hình...")
metrics = model.evaluate(x_test, y_test)
print(f"Loss: {metrics[0]:.4f}, Accuracy: {metrics[1]:.4f}")

# Lưu mô hình
model.save('models/Sequential.keras')  # Thêm đuôi .keras
print("Đã lưu mô hình vào models/Sequential")