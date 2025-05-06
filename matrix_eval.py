import os
import numpy as np
from PIL import Image
from sklearn.metrics import recall_score, precision_score, f1_score, accuracy_score
import pandas as pd

# Fungsi memuat dan konversi citra ke biner
def load_binary_image(image_path, size=(1008, 1008)):
    image = Image.open(image_path).convert("L")
    image = image.resize(size)
    binary = np.array(image) > 127  # threshold
    return binary

# Ganti dengan direktori folder kamu
original_folder = r"D:\Disertasi Bu Sussi\11 April\file pilihan\Eval\Tilling"
generated_folder = r"D:\Disertasi Bu Sussi\11 April\file pilihan\Eval\Obia 0\Fuzzy"

# Ambil semua nama file dari folder asli
image_files = [f for f in os.listdir(original_folder) if f.endswith(('.png', '.jpg'))]

# List hasil evaluasi
results = []

for filename in image_files:
    original_path = os.path.join(original_folder, filename)
    generated_path = os.path.join(generated_folder, filename)
    
    if not os.path.exists(generated_path):
        print(f"Skipping {filename} karena tidak ditemukan di folder buatan.")
        continue
    
    # Load sebagai citra biner
    img1 = load_binary_image(original_path)
    img2 = load_binary_image(generated_path)

    # Flatten
    y_true = img1.flatten()
    y_pred = img2.flatten()

    # Hitung metrik
    recall = recall_score(y_true, y_pred, zero_division=0)
    precision = precision_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    acc = accuracy_score(y_true, y_pred)

    results.append({
        "Filename": filename,
        "Recall": recall,
        "Precision": precision,
        "F1 Score": f1,
        "Accuracy": acc
    })

# Konversi ke DataFrame
df_results = pd.DataFrame(results)

# Hitung rata-rata
average_row = {
    "Filename": "RATA-RATA",
    "Recall": df_results["Recall"].mean(),
    "Precision": df_results["Precision"].mean(),
    "F1 Score": df_results["F1 Score"].mean(),
    "Accuracy": df_results["Accuracy"].mean()
}

# Tambahkan ke bawah DataFrame
df_results = pd.concat([df_results, pd.DataFrame([average_row])], ignore_index=True)

# Tampilkan
print(df_results)

# Simpan ke Excel
df_results.to_excel(r"D:\Disertasi Bu Sussi\11 April\file pilihan\Eval\Fuzzy-obia 0 - 2-1.xlsx", index=False)
