from PIL import Image, ImageOps, ImageFile
import matplotlib.pyplot as plt
import numpy as np
import os

# -----------------------
# FIX untuk gambar besar
# -----------------------
Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

# -----------------------
# CONFIG
# -----------------------
titles = ['Ortophoto', 'Annotation', 'Fuzzy logic', 'Fuzzy + AHP', 'Fuzzy Road Connection', 'AHP Road Connection']
image_paths = [
    [r'D:\Disertasi Bu Sussi\11 April\file pilihan\citra\merge_20_0005.png',
     r'D:\Disertasi Bu Sussi\11 April\file pilihan\citra 5\image-5_tebal.png',
     r'D:\Disertasi Bu Sussi\11 April\file pilihan\citra 5\citra 5 Fuzzy.png',
     r'D:\Disertasi Bu Sussi\11 April\file pilihan\citra 5\citra 5 AHP.png',
     r'D:\Disertasi Bu Sussi\11 April\file pilihan\citra 5\citra 5 Fuzzy hasil.png',
     r'D:\Disertasi Bu Sussi\11 April\file pilihan\citra 5\citra 5 AHP hasil.png']
]
bg_color = (255, 255, 255)
cell_dim = (1024, 1024)  # Ukuran tiap sel (4096 / 4 = 1024)

# -----------------------
# Fungsi Resize & Padding
# -----------------------
def resize_proportional(img, max_size):
    w, h = img.size
    scale = min(max_size[0] / w, max_size[1] / h)
    new_size = (int(w * scale), int(h * scale))
    return img.resize(new_size, Image.Resampling.LANCZOS)

def resize_and_pad(img, target_size, color=(255, 255, 255)):
    img = resize_proportional(img, target_size)
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
        resized_img = resize_and_pad(img, cell_dim, color=bg_color)
        new_row.append(resized_img)
    images_grid.append(new_row)

# -----------------------
# Tampilkan Grid
# -----------------------
nrows = len(images_grid)
ncols = len(titles)

fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(40.96, 40.96), dpi=100)

# Normalisasi bentuk axes agar selalu 2D
if nrows == 1:
    axes = np.expand_dims(axes, axis=0)
if ncols == 1:
    axes = np.expand_dims(axes, axis=1)

for i in range(nrows):
    for j in range(ncols):
        axes[i, j].imshow(images_grid[i][j])
        axes[i, j].axis('off')
        if i == 0:
            axes[i, j].set_title(titles[j], fontsize=20)

plt.tight_layout()
plt.subplots_adjust(wspace=0.05, hspace=0.2)

# -----------------------
# Simpan Hasil
# -----------------------
output_path = r"D:\Disertasi Bu Sussi\11 April\file pilihan\grid\Grid-1 Citra 5.png"
fig.savefig(output_path, dpi=100, bbox_inches='tight')
plt.show()
