import os
import numpy as np
from skimage import io, img_as_ubyte
from skimage.morphology import skeletonize, binary_dilation, disk
from skimage.measure import label, regionprops
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


# Load and preprocess the image
def load_image(image_path):
    image = io.imread(image_path)
    if len(image.shape) == 3:  # Convert to grayscale if RGB
        image = image[:, :, 0]  # Extract red channel for processing
    return image > 128  # Convert to binary

# Apply skeletonization and dilation
def process_skeleton(binary_image, distance= 13):
    skeleton = skeletonize(binary_image)  # Initial skeleton
    dilated = binary_dilation(skeleton, disk(distance))  # Dilate skeleton
    final_skeleton = skeletonize(dilated)  # Re-skeletonize after dilation
    return final_skeleton

# Analyze particles (connected regions)
def analyze_particles(binary_image, min_size=13):
    labeled = label(binary_image)
    cleaned = np.zeros_like(binary_image)
    for region in regionprops(labeled):
        if region.area >= min_size:  # Filter regions by size
            for coord in region.coords:
                cleaned[coord[0], coord[1]] = 1
    return cleaned

# Main processing workflow
def process_images_in_folder(folder_path):
    # List all files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.tif', '.bmp'))]

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        print(f"Processing {image_file}...")

        binary_image = load_image(image_path)
        skeleton = process_skeleton(binary_image, distance=13)
        analyzed = analyze_particles(skeleton, min_size=5)
        final_skeleton = skeletonize(analyzed)  # Final skeletonization

        # Tebalkan garis hasil skeletonisasi
        thickened_skeleton = binary_dilation(final_skeleton, disk(3))

        # Save the result (without displaying)
        result_path = os.path.join(output, f"sambungan_0_{image_file}")
        io.imsave(result_path, img_as_ubyte(thickened_skeleton))
        print(f"Saved processed image as {result_path}")

# Example usage
folder_path = r"D:\Disertasi Bu Sussi\20-Maret\citra 5\Convert\AHP-1"# Replace with the path to your folder containing images
output = r'D:\Disertasi Bu Sussi\20-Maret\citra 5\Sambung\AHP-1'
process_images_in_folder(folder_path)