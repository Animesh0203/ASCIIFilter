from PIL import Image, ImageFilter
import numpy as np
from numba import jit, cuda 


@jit(target_backend='cuda')   
def sobel_filter(image_path, output_path, threshold=18):
    # Load the image
    img = Image.open(image_path)
    
    # Convert the image to grayscale
    img_gray = img.convert('L')
    
    # Convert image to numpy array
    img_array = np.array(img_gray)
    
    # Define Sobel kernels
    Sobel_X = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])
    
    Sobel_Y = np.array([[-1, -2, -1],
                        [ 0,  0,  0],
                        [ 1,  2,  1]])
    
    # Apply Sobel kernels using convolution
    gradient_x = convolve(img_array, Sobel_X)
    gradient_y = convolve(img_array, Sobel_Y)
    
    # Compute magnitude of gradients
    gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    
    # Apply thresholding to highlight edges
    edge_mask = (gradient_magnitude > threshold) * 255
    
    # Convert numpy array back to image
    edge_image = Image.fromarray(edge_mask.astype(np.uint8))
    
    # Save or display the resulting image
    edge_image.save(output_path)
    print(f"Sobel filtered image saved as {output_path}")

def convolve(image, kernel):
    # Get image and kernel dimensions
    img_height, img_width = image.shape
    kernel_size = kernel.shape[0]
    
    # Calculate padding needed
    padding = kernel_size // 2
    
    # Create empty output image
    output = np.zeros_like(image)
    
    # Apply convolution
    for y in range(padding, img_height - padding):
        for x in range(padding, img_width - padding):
            output[y, x] = np.sum(image[y-padding:y+padding+1, x-padding:x+padding+1] * kernel)
    
    return output

# Example usage
input_image = 'dog_image.jpg'
output_image = 'sobel_output.jpg'
sobel_filter(input_image, output_image)
