from PIL import Image
import numpy as np
import os


def quantize_luminance(luminance, n):
    return np.floor(luminance * n) / n


def quantize_image(image_path, output_path, n=10):
    img = Image.open(image_path)

    img_gray = img.convert('L')

    img_array = np.array(img_gray)

    img_norm = img_array / 255.0

    img_quantized = quantize_luminance(img_norm, n)

    img_quantized = (img_quantized * 255).astype(np.uint8)

    img_result = Image.fromarray(img_quantized, mode='L')

    img_result.save(output_path)

    print(f"Quantized image saved as {output_path}")


# Usage
input_path = 'Downscaled'
output_path = 'QuantLumi'

# Ensure the output folder exists
os.makedirs(output_path, exist_ok=True)

# Iterate over all files in the input path
for filename in os.listdir(input_path):
    input_path = os.path.join(input_path, filename)

    # Check if the file is an image by attempting to open it
    try:
        img = Image.open(input_path)
        img.verify()  # Verify that this is an image
        img.close()  # Close the image after verification

        output_path = os.path.join(output_path, filename)
        quantize_image(input_path, output_path, n=10)
    except (IOError, SyntaxError) as e:
        print(f"Skipping {filename}: not a valid image")
