import cv2
import numpy as np

def merge_images_vertical(image_path1, image_path2, output_path):
    # Membaca dua citra
    img1 = cv2.imread(image_path1)
    img2 = cv2.imread(image_path2)
    
    # Cek apakah gambar berhasil dibaca
    if img1 is None:
        print(f"Error: Tidak dapat membaca gambar pertama di {image_path1}")
        return
    if img2 is None:
        print(f"Error: Tidak dapat membaca gambar kedua di {image_path2}")
        return

    # Pastikan kedua citra memiliki lebar yang sama
    width = min(img1.shape[1], img2.shape[1])
    img1 = cv2.resize(img1, (width, img1.shape[0]))
    img2 = cv2.resize(img2, (width, img2.shape[0]))
    
    # Menggabungkan citra secara vertikal
    merged_image = np.vstack((img1, img2))
    
    # Menyimpan hasil citra yang telah digabung
    cv2.imwrite(output_path, merged_image)
    print(f"Citra berhasil digabung dan disimpan di {output_path}")

# Contoh penggunaan dengan path yang diperbaiki
merge_images_vertical(
    r'D:\Disertasi Bu Sussi\11 April\file pilihan\AHP\0\Final\sambungan_0_modified_merge_20_0005_result.png', 
    r'D:\Disertasi Bu Sussi\11 April\file pilihan\AHP\0\Final\sambungan_0_modified_merge_20_0013_result.png', 
    r'D:\Disertasi Bu Sussi\11 April\file pilihan\5 dan 13\final\merge_AHP-hasil.png'
)
