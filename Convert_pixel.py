import os
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

# Fungsi untuk mengubah resolusi gambar
def ubah_resolusi_folder(input_folder, output_folder, ukuran_baru=(1008, 1008)):
    # Membuat folder output jika belum ada
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterasi melalui semua file di folder input
    for file_name in os.listdir(input_folder):
        input_path = os.path.join(input_folder, file_name)
        
        # Memastikan hanya memproses file gambar
        if os.path.isfile(input_path) and file_name.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif')):
            try:
                # Membuka gambar
                with Image.open(input_path) as img:
                    img_resized = img.resize(ukuran_baru)
                    output_path = os.path.join(output_folder, file_name)
                    img_resized.save(output_path)
                    print(f"Berhasil mengubah resolusi: {file_name}")
            except Exception as e:
                print(f"Gagal memproses file {file_name}: {e}")

input_folder = r'D:\Disertasi Bu Sussi\11 April\0%'
output_folder = r'D:\Disertasi Bu Sussi\11 April\AHP-1\All\kecil'  

ubah_resolusi_folder(input_folder, output_folder)