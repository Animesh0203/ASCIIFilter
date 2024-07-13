import numpy as np
from PIL import Image
from numba import cuda, float32

# CUDA kernel for convolution
@cuda.jit
def convolve_kernel(image, kernel, output):
    img_height, img_width = image.shape
    kernel_size = kernel.shape[0]
    padding = kernel_size // 2
    
    y, x = cuda.grid(2)
    
    if padding <= y < img_height - padding and padding <= x < img_width - padding:
        pixel_value = 0.0
        for i in range(kernel_size):
            for j in range(kernel_size):
                pixel_value += image[y + i - padding, x + j - padding] * kernel[i, j]
        output[y, x] = pixel_value

# Sobel filter function with CUDA acceleration and high thresholding
def sobel_filter(image_path, output_path, high_threshold=100):
    # Load the image
    img = Image.open(image_path)
    
    # Convert the image to grayscale
    img_gray = img.convert('L')
    
    # Convert image to numpy array (float32 for CUDA compatibility)
    img_array = np.array(img_gray, dtype=np.float32)
    
    # Define Sobel kernels
    Sobel_X = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]], dtype=np.float32)
    
    Sobel_Y = np.array([[-1, -2, -1],
                        [ 0,  0,  0],
                        [ 1,  2,  1]], dtype=np.float32)
    
    # Allocate device memory for input image, kernels, and output image
    d_img_array = cuda.to_device(img_array)
    d_gradient_x = cuda.device_array_like(img_array)
    d_gradient_y = cuda.device_array_like(img_array)
    
    # Define block and grid dimensions for CUDA kernel launch
    threads_per_block = (16, 16)
    blocks_per_grid_x = (img_array.shape[0] + threads_per_block[0] - 1) // threads_per_block[0]
    blocks_per_grid_y = (img_array.shape[1] + threads_per_block[1] - 1) // threads_per_block[1]
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)
    
    # Launch CUDA kernels for convolution
    convolve_kernel[blocks_per_grid, threads_per_block](d_img_array, Sobel_X, d_gradient_x)
    convolve_kernel[blocks_per_grid, threads_per_block](d_img_array, Sobel_Y, d_gradient_y)
    
    # Copy results back from device to host
    gradient_x = d_gradient_x.copy_to_host()
    gradient_y = d_gradient_y.copy_to_host()
    
    # Compute magnitude of gradients
    gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    
    # Apply thresholding to detect only super high changes in edges
    edge_mask = np.zeros_like(gradient_magnitude, dtype=np.uint8)
    edge_mask[gradient_magnitude <= high_threshold] = 255
    
    # Convert numpy array back to image
    edge_image = Image.fromarray(edge_mask)
    
    # Save or display the resulting image
    edge_image.save(output_path)
    print(f"Sobel filtered image saved as {output_path}")

# Example usage with custom high threshold
input_image = 'dog_image.jpg'
output_image = 'sobel_output_high_threshold.jpg'
sobel_filter(input_image, output_image, high_threshold=150)
