from PIL import Image, ImageOps
import numpy as np

def increase_contrast(image_path, output_path, contrast_factor=1.5):
    # Load the image
    img = Image.open(image_path)
    
    # Convert the image to grayscale
    img_gray = ImageOps.grayscale(img)
    
    # Convert image to numpy array
    img_array = np.array(img_gray)
    
    # Calculate image statistics
    min_val = np.min(img_array)
    max_val = np.max(img_array)
    
    # Perform contrast stretching
    img_array = (img_array - min_val) / (max_val - min_val)
    img_array = np.clip(img_array, 0, 1)  # Clip values to ensure they are within valid range
    
    # Increase contrast by multiplying by contrast_factor
    img_array = img_array * contrast_factor
    
    # Convert back to uint8 and create PIL image
    img_contrast = Image.fromarray((img_array * 255).astype(np.uint8))
    
    # Save or display the resulting image
    img_contrast.save(output_path)
    print(f"Contrast enhanced image saved as {output_path}")

# Example usage
input_image = 'QuantLumi/counter.jpg'
output_image = 'QuantLumi/Image.jpg'
increase_contrast(input_image, output_image, contrast_factor=1.5)
