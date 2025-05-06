import cv2
import numpy as np
import os

# Folder input dan output
input_folder = r"D:\Disertasi Bu Sussi\20-Maret\citra 5\Sambung\AHP-1"
output_folder = r"D:\Disertasi Bu Sussi\20-Maret\citra 5\Final\AHP-1"

# Pastikan folder output ada
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Tentukan ambang batas panjang minimum untuk mempertahankan garis
min_length = 750  # Sesuaikan nilai ini sesuai kebutuhan

# Proses setiap gambar dalam folder
for filename in os.listdir(input_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        
        # Path lengkap untuk membaca dan menyimpan gambar
        image_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        # Load gambar asli
        image = cv2.imread(image_path)
        if image is None:
            print(f"Gagal membaca {filename}, lewati...")
            continue
        
        # Konversi ke grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Terapkan threshold untuk mendapatkan gambar biner
        _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
        
        # Deteksi kontur
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Buat mask untuk menyimpan garis utama
        filtered_mask = np.ones_like(gray) * 255  # Background putih
        
        # Gambar ulang hanya kontur yang panjangnya cukup besar, yang kecil dihapus
        for contour in contours:
            if cv2.arcLength(contour, closed=False) > min_length:
                cv2.drawContours(filtered_mask, [contour], -1, 0, thickness=1)  # Garis utama tetap hitam
            else:
                cv2.drawContours(image, [contour], -1, (0, 0, 0), thickness=cv2.FILLED)  # Hapus garis kecil
        
        # Simpan hasil
        cv2.imwrite(output_path, image)
        print(f"Diproses: {filename} -> {output_path}")

print("Selesai memproses semua gambar.")
