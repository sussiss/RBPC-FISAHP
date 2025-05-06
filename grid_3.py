from PIL import Image, ImageOps, ImageFile
import matplotlib.pyplot as plt
import os

# -----------------------
# FIX untuk gambar besar
# -----------------------
Image.MAX_IMAGE_PIXELS = None  # Disable DecompressionBombError
ImageFile.LOAD_TRUNCATED_IMAGES = True  # Handle file besar

# -----------------------
# CONFIG
# -----------------------
titles = ['Ortophoto', 'Annotation', 'Fuzzy OBIA 0%', 'Fuzzy OBIA 25%', 'Fuzzy Refinement OBIA 50%', 'Artery OBIA 0%', 'Artery OBIA 25%', 'Artery Refinement OBIA 50%']
image_paths = [
    [r'11 April\file pilihan\citra\merge_20_0020.png', #ortho
     r'11 April\file pilihan\final\hitam putih\image-20_tebal.png', #tilling
     r'11 April\file pilihan\Fuzzy\0\new color\merge_20_0020_result.png', #obia 0
     r'11 April\file pilihan\Fuzzy\25\new color\merge_20_0020_result.png', #obia 25
     r'11 April\file pilihan\Fuzzy\50\new color\merge_20_0020_result.png', #obia 50
     r'11 April\file pilihan\Fuzzy\0\Final\sambungan_0_merge_20_0020_result.png', #h obia 0
     r'11 April\file pilihan\Fuzzy\25\final\sambungan_0_merge_20_0020_result.png', #h obia 25
     r'11 April\file pilihan\Fuzzy\50\final\sambungan_0_merge_20_0020_result.png'],  #h obia 50
    [r'11 April\file pilihan\citra\merge_20_0044.png', #ortho
     r'11 April\file pilihan\final\hitam putih\image-44_tebal.png', #tilling
     r'11 April\file pilihan\Fuzzy\0\new color\merge_20_0044_result.png', #obia 0
     r'11 April\file pilihan\Fuzzy\25\new color\merge_20_0044_result.png', #obia 25
     r'11 April\file pilihan\Fuzzy\50\new color\merge_20_0044_result.png', #obia 50
     r'11 April\file pilihan\Fuzzy\0\Final\sambungan_0_merge_20_0044_result.png', #h obia 0
     r'11 April\file pilihan\Fuzzy\25\final\sambungan_0_merge_20_0044_result.png', #h obia 25
     r'11 April\file pilihan\Fuzzy\50\final\sambungan_0_merge_20_0044_result.png'],  #h obia 50
     [r'11 April\file pilihan\citra\merge_20_0045.png', #ortho
     r'11 April\file pilihan\final\hitam putih\image-45_tebal.png', #tilling
     r'11 April\file pilihan\Fuzzy\0\new color\merge_20_0045_result.png', #obia 0
     r'11 April\file pilihan\Fuzzy\25\new color\merge_20_0045_result.png', #obia 25
     r'11 April\file pilihan\Fuzzy\50\new color\merge_20_0045_result.png', #obia 50
     r'11 April\file pilihan\Fuzzy\0\Final\sambungan_0_merge_20_0045_result.png', #h obia 0
     r'11 April\file pilihan\Fuzzy\25\final\sambungan_0_merge_20_0045_result.png', #h obia 25
     r'11 April\file pilihan\Fuzzy\50\final\sambungan_0_merge_20_0045_result.png'],  #h obia 50
     [r'11 April\file pilihan\citra\merge_20_0077.png', #ortho
     r'11 April\file pilihan\final\hitam putih\image-77_tebal.png', #tilling
     r'11 April\file pilihan\Fuzzy\0\new color\merge_20_0077_result.png', #obia 0
     r'11 April\file pilihan\Fuzzy\25\new color\merge_20_0077_result.png', #obia 25
     r'11 April\file pilihan\Fuzzy\50\new color\merge_20_0077_result.png', #obia 50
     r'11 April\file pilihan\Fuzzy\0\Final\sambungan_0_merge_20_0077_result.png', #h obia 0
     r'11 April\file pilihan\Fuzzy\25\final\sambungan_0_merge_20_0077_result.png', #h obia 25
     r'11 April\file pilihan\Fuzzy\50\final\sambungan_0_merge_20_0077_result.png'],  #h obia 50
]
bg_color = (255, 255, 255)  # white background
max_dim = (4096, 4096)  # batas maksimum panjang dan lebar

# -----------------------
# Fungsi Resize Aman (tanpa crop)
# -----------------------
def resize_proportional(img, max_size):
    w, h = img.size
    scale = min(max_size[0] / w, max_size[1] / h)
    new_size = (int(w * scale), int(h * scale))
    return img.resize(new_size, Image.Resampling.LANCZOS)

def resize_and_pad(img, target_size, color=(255, 255, 255)):
    img = resize_proportional(img, target_size)  # Resize proporsional dulu
    delta_w = target_size[0] - img.size[0]
    delta_h = target_size[1] - img.size[1]
    padding = (delta_w // 2, delta_h // 2, delta_w - delta_w // 2, delta_h - delta_h // 2)
    return ImageOps.expand(img, padding, fill=color)

# -----------------------
# Proses semua gambar
# -----------------------
images_grid = []

for row in image_paths:
    new_row = []
    for path in row:
        img = Image.open(path).convert('RGB')
        resized_img = resize_and_pad(img, max_dim, color=bg_color)
        new_row.append(resized_img)
    images_grid.append(new_row)

# -----------------------
# Tampilkan Grid
# -----------------------
fig, axes = plt.subplots(nrows=len(images_grid), ncols=len(titles), figsize=(12, 6))  # Perkecil figsize

for i in range(len(images_grid)):
    for j in range(len(titles)):
        axes[i, j].imshow(images_grid[i][j])
        axes[i, j].axis('off')
        if i == 0:
            axes[i, j].set_title(titles[j], fontsize=5)

# Gunakan ini, bukan tight_layout
plt.subplots_adjust(wspace=0.01, hspace=0.1)  # Kecilkan jarak antar gambar

plt.show()

fig.savefig(r"D:\Disertasi Bu Sussi\11 April\file pilihan\Grid 3-Fuzzy", dpi=300, bbox_inches='tight')