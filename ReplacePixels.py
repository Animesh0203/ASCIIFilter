from PIL import Image
import numpy as np
import os

def quantize_luminance(luminance, n):
    return np.floor(luminance * n) / n

def create_ascii_image(input_path, output_path, ascii_chars=' .:-=+*#%@', char_image_dir='char_images'):
    # Open the image and convert to grayscale
    img = Image.open(input_path).convert('L')
    width, height = img.size
    
    # Convert to numpy array and normalize
    img_array = np.array(img) / 255.0
    
    # Number of luminance levels is equal to the number of ASCII characters
    n = len(ascii_chars)
        
    # Create a new image for ASCII art (each character will be 8x8 pixels)
    ascii_img = Image.new('L', (width * 8, height * 8), color=0)
    
    # Load character images
    char_images = {}
    for i, char in enumerate(ascii_chars):
        char_img_path = os.path.join(char_image_dir, f"{ord(char):03d}.jpg")
        if os.path.exists(char_img_path):
            char_images[i] = np.array(Image.open(char_img_path).convert('L'))
        else:
            print(f"Warning: Image for character '{char}' not found at {char_img_path}")
            # Create a blank image if the file is not found
            char_images[i] = np.zeros((8, 8), dtype=np.uint8)
    
    # Map quantized luminance to characters and draw
    for y in range(height):
        for x in range(width):
            lum_level = int(img_array[y, x] * (n - 1))
            char_img = char_images[lum_level]
            ascii_img.paste(Image.fromarray(char_img), (x * 8, y * 8))
    
    # Save the result
    ascii_img.save(output_path)
    print(f"ASCII art image saved as {output_path}")

# Usage
input_path = 'QuantLumi'
output_path = 'Output'

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
        create_ascii_image(input_path, output_path, char_image_dir='8_Lumi')
    except (IOError, SyntaxError) as e:
        print(f"Skipping {filename}: not a valid image")

