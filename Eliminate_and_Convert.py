import cv2
import numpy as np
import os

# Fungsi untuk menghitung jarak Euclidean
def euclidean_distance(pt1, pt2):
    return np.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)

def process_images(input_folder, output_folder):
    # Pastikan folder output ada
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop melalui semua file dalam folder input
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Load gambar asli
            image = cv2.imread(image_path)
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            # Hilangkan garis biru
            blue_mask = cv2.inRange(hsv_image, np.array([100, 150, 0]), np.array([140, 255, 255]))
            image[blue_mask > 0] = (0, 0, 0)

            # Deteksi warna merah dan kuning
            red_mask = cv2.inRange(hsv_image, np.array([0, 70, 50]), np.array([10, 255, 255])) | \
                       cv2.inRange(hsv_image, np.array([170, 70, 50]), np.array([180, 255, 255]))
            yellow_mask = cv2.inRange(hsv_image, np.array([25, 100, 100]), np.array([35, 255, 255]))

            # Ambil kontur kuning dari mask kuning langsung (BUKAN edge detection)
            yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Lakukan iterasi untuk memperluas area warna merah
            threshold_distance = 130  # Sesuaikan nilai ini sesuai kebutuhan
            for iteration in range(2):
                # Update seluruh titik garis merah untuk setiap iterasi
                red_edges = cv2.Canny(red_mask, 50, 150)
                red_contours, _ = cv2.findContours(red_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                red_points = [tuple(pt[0]) for cnt in red_contours for pt in cnt]

                next_yellow_contours = []
                for y_cnt in yellow_contours:
                    if any(euclidean_distance(red_pt, tuple(y_pt[0])) <= threshold_distance for red_pt in red_points for y_pt in y_cnt):
                        # Mengisi seluruh area kontur kuning menjadi merah
                        cv2.drawContours(image, [y_cnt], -1, (0, 0, 255), thickness=cv2.FILLED)
                    else:
                        # Simpan kontur kuning yang belum berubah warna untuk iterasi berikutnya
                        next_yellow_contours.append(y_cnt)

                yellow_contours = next_yellow_contours
            
            # Convert to HSV for color detection
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Detect yellow lines
            mask_yellow = cv2.inRange(hsv, np.array([20, 100, 100]), np.array([30, 255, 255]))
            
            # Remove yellow lines by changing them to black
            image[mask_yellow > 0] = [0, 0, 0]
            
            # Simpan hasil akhir
            cv2.imwrite(output_path, image)
            print(f"Processed image saved to: {output_path}")

# Jalankan fungsi dengan folder input dan output yang telah ditentukan
input_folder = r"D:\Disertasi Bu Sussi\11 April\AHP-1\All\kecil"
output_folder = r"D:\Disertasi Bu Sussi\11 April\AHP-1\All\convert"
process_images(input_folder, output_folder)
