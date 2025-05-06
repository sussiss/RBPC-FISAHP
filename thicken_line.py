import cv2
import numpy as np

# Baca gambar
img = cv2.imread(r"D:\Disertasi Bu Sussi\11 April\file pilihan\final\operator\image-77.png")

# Ubah ke grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Threshold agar garis jadi lebih jelas (bisa disesuaikan jika perlu)
_, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

# Temukan kontur dari garis
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Buat gambar kosong (hitam)
thick_lines = np.zeros_like(img)

# Gambar ulang kontur dengan ketebalan lebih
cv2.drawContours(thick_lines, contours, -1, (0, 255, 255), thickness=90)  # Warna kuning cerah (BGR)

# Simpan hasilnya
cv2.imwrite(r"D:\Disertasi Bu Sussi\11 April\file pilihan\final\ditebalkan\image-77_tebal.png", thick_lines)

print("Selesai!")