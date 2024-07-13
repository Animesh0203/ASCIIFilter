from PIL import Image
import os

def downscale_image(input_path, output_path, pixel_size=8):
    # Open the image
    img = Image.open(input_path)
    
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
    
    # Save the result
    result.save(output_path)

# Usage
input_path = 'InputImages'
output_path = 'Downscaled'

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
        downscale_image(input_path, output_path)
    except (IOError, SyntaxError) as e:
        print(f"Skipping {filename}: not a valid image")
