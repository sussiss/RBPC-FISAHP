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
titles = ['Ortophoto', 'Annotation', 'FIS', 'FISAHP', 'RBPC-FIS', 'RBPC-FISAHP']
image_paths = [
    [r'11 April\file pilihan\citra\merge_20_0020.png', #ortho
     r'11 April\file pilihan\final\hitam putih\image-20_tebal.png', #tilling
     r'11 April\file pilihan\Fuzzy\50\new color\merge_20_0020_result.png', #fuzzy
     r'11 April\file pilihan\AHP\50\new color\modified_merge_20_0020_result.png', #ahp
     r'11 April\file pilihan\Fuzzy\50\Final\sambungan_0_merge_20_0020_result.png', #hasil fuzzy
     r'11 April\file pilihan\AHP\50\Final\sambungan_0_modified_merge_20_0020_result.png'], #hasil ahp
    [r'11 April\file pilihan\citra\merge_20_0044.png',
     r'11 April\file pilihan\final\hitam putih\image-44_tebal.png',
     r'11 April\file pilihan\Fuzzy\50\new color\merge_20_0044_result.png',
     r'11 April\file pilihan\AHP\50\new color\modified_merge_20_0044_result.png',
     r'11 April\file pilihan\Fuzzy\50\Final\sambungan_0_merge_20_0044_result.png',
     r'11 April\file pilihan\AHP\50\Final\sambungan_0_modified_merge_20_0044_result.png'],
     [r'11 April\file pilihan\citra\merge_20_0045.png',
     r'11 April\file pilihan\final\hitam putih\image-45_tebal.png',
     r'11 April\file pilihan\Fuzzy\50\new color\merge_20_0045_result.png',
     r'11 April\file pilihan\AHP\50\new color\modified_merge_20_0045_result.png',
     r'11 April\file pilihan\Fuzzy\50\Final\sambungan_0_merge_20_0045_result.png',
     r'11 April\file pilihan\AHP\50\Final\sambungan_0_modified_merge_20_0045_result.png'],
     [r'11 April\file pilihan\citra\merge_20_0077.png',
     r'11 April\file pilihan\final\hitam putih\image-77_tebal.png',
     r'11 April\file pilihan\Fuzzy\50\new color\merge_20_0077_result.png',
     r'11 April\file pilihan\AHP\50\new color\modified_merge_20_0077_result.png',
     r'11 April\file pilihan\Fuzzy\50\Final\sambungan_0_merge_20_0077_result.png',
     r'11 April\file pilihan\AHP\50\Final\sambungan_0_modified_merge_20_0077_result.png']
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
# Tampilkan Grid dengan Label Huruf
# -----------------------
fig, axes = plt.subplots(nrows=len(images_grid), ncols=len(titles), figsize=(12, 8))

labels = ['A', 'B', 'C', 'D']

for i in range(len(images_grid)):
    for j in range(len(titles)):
        axes[i, j].imshow(images_grid[i][j])
        axes[i, j].axis('off')
        if i == 0:
            axes[i, j].set_title(titles[j], fontsize=9)
        if j == 0:
            axes[i, j].text(-0.08, 0.5, labels[i], fontsize=16, fontweight='bold', transform=axes[i, j].transAxes,
                            ha='center', va='center')

plt.subplots_adjust(wspace=0.05, hspace=0.1)

plt.show()

fig.savefig(r"D:\\Disertasi Bu Sussi\\11 April\\file pilihan\\grid 2\\Grid 2-50%.png", dpi=300, bbox_inches='tight')
