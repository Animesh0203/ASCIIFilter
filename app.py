import streamlit as st
from PIL import Image, ImageFile
import numpy as np
import os
import io

# CSS styles
css = """
@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'Roboto Mono', monospace;
    font-size: 18px;
    font-weight: 500;
    color: #091747;
}
"""

# Display the CSS using st.markdown
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


# Set a larger decompression limit
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

def resize_if_necessary(image):
    max_pixels_limit = 178956970  # Limit for decompression bomb
    width, height = image.size
    total_pixels = width * height
    if total_pixels > max_pixels_limit:
        st.warning(f"Image size ({total_pixels} pixels) exceeds limit of {max_pixels_limit} pixels. Resizing the image.")
        image = image.resize((image.width // 4, image.height // 4))
    return image

###################################################
###################################################
###################################################
###################################################
def downscale_image(img, pixel_size):
    # Calculate new dimensions
    width, height = img.size
    new_width = width // pixel_size
    new_height = height // pixel_size
    
    # Resize the image
    img_resized = img.resize((new_width, new_height), Image.NEAREST)
    
    # Create a new image with the original dimensions
    result = Image.new('RGB', (width, height))
    
    # Upscale the resized image
    for y in range(new_height):
        for x in range(new_width):
            color = img_resized.getpixel((x, y))
            for dy in range(pixel_size):
                for dx in range(pixel_size):
                    result.putpixel((x*pixel_size+dx, y*pixel_size+dy), color)
    
    return result

###################################################
###################################################

def quantize_luminance(luminance, n):
    return np.floor(luminance * n) / n

def quantize_image(img, n=10):
    img_gray = img.convert('L')
    img_array = np.array(img_gray)
    img_norm = img_array / 255.0
    img_quantized = quantize_luminance(img_norm, n)
    img_quantized = (img_quantized * 255).astype(np.uint8)
    img_result = Image.fromarray(img_quantized, mode='L')
    return img_result

###################################################
###################################################

def create_ascii_image(img, ascii_chars=' .:-=+*#%■', char_image_dir='8_Lumi'):
    # Convert to grayscale
    img = img.convert('L')
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
            char_img = char_images.get(lum_level, Image.new('L', (8, 8), color=255))
            ascii_img.paste(char_img, (x * 8, y * 8))
    
    return ascii_img
###################################################
###################################################
###################################################
###################################################

st.title("ASCIICORE")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    progress_bar = st.progress(0)
    # Read the image as bytes
    image = Image.open(uploaded_file)

    # Display the image
    st.image(image, caption="Uploaded Image", use_column_width=True)
    progress_bar = st.progress(100)
    st.success('Image Uploaded!')

button1 = st.button("Get ASCII'd")

if button1:
    image = resize_if_necessary(image)
    img = downscale_image(image, 8)
    
    img1 = quantize_image(img, 10)
    
    img2 = create_ascii_image(img1)
    progress_bar = st.progress(100)
    st.image(img2, caption='ASCII Image', use_column_width=True)
    st.success('Processing Complete!')

    ascii_image_bytes = io.BytesIO()
    img2.save(ascii_image_bytes, format='PNG')
    ascii_image_bytes.seek(0)
    st.download_button(label='Download ASCII Image', data=ascii_image_bytes, file_name='ASCIICORE_Image.png', mime='image/png')
        
