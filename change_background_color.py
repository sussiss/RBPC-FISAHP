import cv2
import numpy as np
import os

# Path folder input dan output
input_folder = r"D:\Disertasi Bu Sussi\11 April\file pilihan\final\ditebalkan"       # Ganti dengan path folder kamu
output_folder = r"D:\Disertasi Bu Sussi\11 April\file pilihan\final\hitam putih"     # Ganti sesuai keinginan

# Buat folder output jika belum ada
os.makedirs(output_folder, exist_ok=True)

# Fungsi untuk ubah kuning jadi putih
def convert_yellow_to_white(image_path, save_path):
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Rentang warna kuning (bisa disesuaikan)
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([40, 255, 255])

    # Deteksi warna kuning
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Ubah jadi putih
    result = img.copy()
    result[mask > 0] = [255, 255, 255]

    # Simpan hasil
    cv2.imwrite(save_path, result)

# Proses semua gambar dalam folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        convert_yellow_to_white(input_path, output_path)
        print(f"Processed: {filename}")

print("Selesai! Semua gambar telah diproses.")
