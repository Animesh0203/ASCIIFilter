from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

def render_character(char, output_path, size):
    # Create a new 8x8 black image
    img = Image.new('L', (size, size), color=0)
    
    # Create a drawing object
    draw = ImageDraw.Draw(img)
    
    # Try to load a system font, fall back to default if not found
    try:
        # For Windows
        font = ImageFont.truetype("arial.ttf", size)
    except OSError:
        try:
            # For macOS
            font = ImageFont.truetype("/Library/Fonts/Arial.ttf", size)
        except OSError:
            try:
                # For Linux
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size)
            except OSError:
                # If all else fails, use default font
                font = ImageFont.load_default()
    
    # Calculate text width and use font size for height
    text_width = draw.textlength(char, font=font)
    text_height = font.size
    
    # Calculate position to center the character
    position = ((size - text_width) // 2, (size - text_height) // 2)
    
    # Draw the character in white
    draw.text(position, char, fill=255, font=font)
    
    # Save the image
    img.save(output_path)
    
    print(f"Character rendered and saved as {output_path}")
    
    # Convert to numpy array and print (for visualization in console)
    img_array = np.array(img)
    print(img_array)

# Usage
for char in ' .:-=+*#%■':
    ascii_value = ord(char)
    output_filename = f"{ascii_value:03}.jpg"  # Format as three-digit number with leading zeros
    output_path = os.path.join('8_Lumi', output_filename)
    render_character(char, output_path, 64)  # Take only the first character if more are entered