from PIL import Image, ImageDraw, ImageFont
import numpy as np

def get_ascii_char(intensity, ascii_chars):
    return ascii_chars[int(intensity * (len(ascii_chars) - 1))]

def image_to_ascii(image_path, output_path, width=100, ascii_chars=' .:-=+*#%@'):
    # Open image and resize
    image = Image.open(image_path)
    aspect_ratio = image.height / image.width
    height = int(aspect_ratio * width * 0.55)
    image = image.resize((width, height))
    
    # Convert to grayscale
    image = image.convert('L')
    
    # Create a new image for ASCII art
    font="Pillow/Tests/fonts/FreeMono.ttf"
    char_width, char_height = font.getsize('A')
    out_width = char_width * width
    out_height = char_height * height
    out_image = Image.new('L', (out_width, out_height), color=255)
    draw = ImageDraw.Draw(out_image)
    
    # Generate ASCII art
    pixels = np.array(image)
    for i in range(height):
        for j in range(width):
            intensity = pixels[i, j] / 255.0
            char = get_ascii_char(intensity, ascii_chars)
            draw.text((j * char_width, i * char_height), char, font=font, fill=0)
    
    # Save the result
    out_image.save(output_path)

# Usage
image_to_ascii('image.jpeg', 'ascii_output.png', width=100)