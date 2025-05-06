import cv2
import numpy as np
import pandas as pd
import os
from skfuzzy import control as ctrl
import skfuzzy as fuzz

# Konstanta resolusi
PIXEL_TO_KM = 1 / 20000  # Resolusi 5 cm/piksel, jadi 1 km = 20.000 piksel

# Fungsi untuk menghitung panjang garis dalam kilometer
def calculate_length_in_km(length_in_pixels):
    return length_in_pixels * PIXEL_TO_KM

# Fungsi keanggotaan fuzzy
def create_fuzzy_system():
    # Membership untuk panjang jalan
    
    length = ctrl.Antecedent(np.arange(-0.4, 0.75, 0.01), 'length')
    length['short'] = fuzz.trapmf(length.universe, [-0.4, -0.4, 0.01, 0.03])
    length['medium'] = fuzz.trapmf(length.universe, [0.02, 0.09, 0.15, 0.2])
    length['long'] = fuzz.trapmf(length.universe, [0.17, 0.3, 0.75, 0.75])

    # Membership untuk kurvatur
    curvature = ctrl.Antecedent(np.arange(0.5, 2.5, 0.001), 'curvature')
    curvature['straight'] = fuzz.trapmf(curvature.universe, [0.5, 0.5, 1.0, 1.2])
    curvature['slightly_curved'] = fuzz.trapmf(curvature.universe, [1.1, 1.3, 1.7, 1.9])
    curvature['sharp_curved'] = fuzz.trapmf(curvature.universe, [1.8, 2.0, 2.5, 2.5])

    # Membership untuk artery
    artery = ctrl.Consequent(np.arange(0.4, 1.0, 0.001), 'artery')
    artery['small'] = fuzz.trapmf(artery.universe, [0.4, 0.4, 0.5, 0.6])
    artery['medium'] = fuzz.trapmf(artery.universe, [0.55, 0.65, 0.75, 0.85])
    artery['large'] = fuzz.trapmf(artery.universe, [0.8, 0.9, 1.0, 1.0])

    # Aturan fuzzy
    rules = [
        ctrl.Rule(length['short'] & curvature['straight'], artery['small']),
        ctrl.Rule(length['short'] & curvature['slightly_curved'], artery['small']),
        ctrl.Rule(length['short'] & curvature['sharp_curved'], artery['large']),
        ctrl.Rule(length['medium'] & curvature['straight'], artery['medium']),
        ctrl.Rule(length['medium'] & curvature['slightly_curved'], artery['medium']),
        ctrl.Rule(length['medium'] & curvature['sharp_curved'], artery['medium']),
        ctrl.Rule(length['long'] & curvature['straight'], artery['large']),
        ctrl.Rule(length['long'] & curvature['slightly_curved'], artery['large']),
        ctrl.Rule(length['long'] & curvature['sharp_curved'], artery['small']),
    ]

    # Sistem kontrol fuzzy
    artery_ctrl = ctrl.ControlSystem(rules)
    return ctrl.ControlSystemSimulation(artery_ctrl)

# Fungsi menghitung kurvatur
def calculate_curvature(points):
    if len(points) < 3:
        return 0
    curvature = 0
    for i in range(1, len(points)-1):
        p1 = np.array(points[i - 1], dtype=np.float32)
        p2 = np.array(points[i], dtype=np.float32)
        p3 = np.array(points[i + 1], dtype=np.float32)
        v1 = p2 - p1
        v2 = p3 - p2
        angle = np.arccos(
            np.clip(
                np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-8),
                -1.0,
                1.0
            )
        )
        curvature += angle
    return curvature / (len(points) - 2)    

# Input folder dan output folder
input_folder = r"D:\Disertasi Bu Sussi\20-Maret\citra 5\obia\merge".strip()
output_folder = r"D:\Disertasi Bu Sussi\20-Maret\citra 5\Fuzzy".strip()

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Inisialisasi sistem fuzzy
fuzzy_system = create_fuzzy_system()

# Proses setiap gambar di folder
for file_name in os.listdir(input_folder):
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(input_folder, file_name)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            print(f"Error: Gagal memuat gambar {file_name}")
            continue

        # Preprocessing steps
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        equalized = cv2.equalizeHist(blurred)
        edges = cv2.Canny(equalized, 30, 100)

        # Dilate edges
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        dilated_edges = cv2.dilate(edges, kernel, iterations=2)

        # Find contours
        contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Konversi citra grayscale ke BGR untuk memungkinkan pewarnaan
        output_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        # Hasil
        results = []

        # Proses setiap kontur
        for idx, contour in enumerate(contours):
            length_in_pixels = cv2.arcLength(contour, True)
            length_in_km = calculate_length_in_km(length_in_pixels)

            # Hitung kurvatur
            curvature_value = calculate_curvature(contour[:, 0, :])

            # Masukkan nilai ke sistem fuzzy
            fuzzy_system.input['length'] = length_in_km
            fuzzy_system.input['curvature'] = curvature_value
            fuzzy_system.compute()

            # Nilai output dari sistem fuzzy (defuzzifikasi)
            artery_value = fuzzy_system.output['artery']
            if artery_value < 0.65:
                label = f"small_artery_{idx:03}"
                color = (255, 0, 0) # biru untuk arteri kecil
            elif 0.5 <= artery_value < 0.85:
                label = f"medium_artery_{idx:03}"
                color = (0, 255, 255)      # Kuning untuk arteri sedang
            else:
                label = f"big_artery_{idx:03}"
                color = (0, 0, 255)        # Merah untuk arteri besar

            # Buat mask untuk kontur saat ini
            mask = np.zeros_like(image, dtype=np.uint8)
            cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

            # Terapkan warna pada output_image menggunakan mask
            output_image[mask == 255] = color

            # Gambar label di lokasi kontur
            # x, y, _, _ = cv2.boundingRect(contour)
            # named_label = f"{idx:03}"

            # font_scale = 4
            # font_thickness = 2
            # cv2.putText(output_image,named_label,(x,y -10), cv2.FONT_HERSHEY_SIMPLEX,font_scale,color,font_thickness,cv2.LINE_AA)

            # Simpan hasil
            results.append({
                "Line_ID": label,
                "Length (km)": length_in_km,
                "Curvature": curvature_value,
                "Artery Membership Value": f"{artery_value:.3f}"
            })

        # Simpan hasil
        base_name = os.path.splitext(file_name)[0]
        csv_path = os.path.join(output_folder, f"{base_name}_result.csv")
        image_output_path = os.path.join(output_folder, f"{base_name}_result.png")
        
        # Simpan CSV dan gambar
        df = pd.DataFrame(results)
        df.to_csv(csv_path, index=False)
        cv2.imwrite(image_output_path, output_image)

        print(f"Proses selesai untuk {file_name}. Hasil disimpan di {output_folder}.")