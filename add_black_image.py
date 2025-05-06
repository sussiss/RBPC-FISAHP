import cv2
import os
import numpy as np

def create_missing_black_images(source_folder, output_folder, total_images=96):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Dapatkan daftar file yang ada di folder sumber
    existing_files = [f for f in os.listdir(source_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    existing_files.sort()

    print(f"Jumlah file ditemukan di {source_folder}: {len(existing_files)}")

    # Mengekstrak indeks file yang ada
    existing_indices = set()
    for f in existing_files:
        try:
            idx = int(f.split('_')[-2])  # Ambil angka sebelum "_result.png"
            existing_indices.add(idx)
        except ValueError:
            print(f"Format file tidak sesuai: {f}")

    # Pastikan ada minimal 1 file untuk referensi ukuran
    if existing_files:
        sample_img = cv2.imread(os.path.join(source_folder, existing_files[0]))
        if sample_img is None:
            print("Gagal membaca gambar referensi! Cek format file.")
            return
        
        height, width, channels = sample_img.shape
        print(f"Ukuran gambar referensi: {height}x{width}, Channels: {channels}")
    else:
        print("Tidak ada gambar referensi yang ditemukan!")
        return

    # Buat gambar hitam hanya jika file dengan indeks tertentu tidak ada
    for i in range(1, total_images + 1):
        filename = f"sambungan_0_modified_modified_merge_20_{i:04d}_result.png"
        output_path = os.path.join(output_folder, filename)

        if i not in existing_indices:  # Jika file tidak ada, buat gambar hitam
            black_image = np.zeros((height, width, channels), dtype=np.uint8)
            cv2.imwrite(output_path, black_image)
            print(f"Membuat gambar hitam: {filename}")
        else:
            print(f"File sudah ada: {filename}")

# Contoh penggunaan:
source_folder = r"D:\Disertasi Bu Sussi\20-Maret\citra 5\Sambung\Fuzzy"   # Folder gambar asli
output_folder = r"D:\Disertasi Bu Sussi\20-Maret\citra 5\Final\Fuzzy"  # Folder output
total_images = 96  # Jumlah total gambar yang diharapkan

create_missing_black_images(source_folder, output_folder, total_images)
