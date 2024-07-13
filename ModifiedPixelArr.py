from PIL import Image, ImageDraw, ImageFont
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
    
    # Create a new image for ASCII art
    ascii_img = Image.new('RGB', (width * 8, height * 8), color=(255, 255, 255))
    
    # Load character images
    char_images = {}
    for i, char in enumerate(ascii_chars):
        char_img_path = os.path.join(char_image_dir, f"{ord(char):03d}.jpg")
        if os.path.exists(char_img_path):
            char_images[i] = Image.open(char_img_path).convert('L')
        else:
            print(f"Warning: Image for character '{char}' not found at {char_img_path}")
            # Create a blank image if the file is not found
            char_images[i] = Image.new('L', (8, 8), color=255)
    
    # Calculate the luminance for each 8x8 block and map to characters
    for y in range(0, height, 8):
        for x in range(0, width, 8):
            # Get the average luminance of the 8x8 block
            block = img_array[y:y+8, x:x+8]
            avg_luminance = np.mean(block)
            lum_level = int(avg_luminance * (n - 1))
            char_img = char_images[lum_level]
            ascii_img.paste(char_img, (x * 8, y * 8))
    
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
