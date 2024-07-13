from PIL import Image, ImageFilter
import numpy as np

# Load the image
image = Image.open('BLEACH Mobile Wallpaper #1398387 - Zerochan Anime Image Board.jpeg')
# Apply the first Gaussian blur with sigma1
sigma1 = 1
blurred_image1 = image.filter(ImageFilter.GaussianBlur(sigma1))

# Apply the second Gaussian blur with sigma2
sigma2 = 200
blurred_image2 = image.filter(ImageFilter.GaussianBlur(sigma2))
# Convert images to NumPy arrays
blurred_array1 = np.array(blurred_image1)
blurred_array2 = np.array(blurred_image2)

# Subtract the two arrays
dog_array = blurred_array1 - blurred_array2

# Clip the values to be in the valid range (0-255) and convert back to uint8
dog_array = np.clip(dog_array, 0, 255).astype(np.uint8)

# Convert the result back to an image
dog_image = Image.fromarray(dog_array)
# Save the resulting image
dog_image.save('dog_image.jpg')

# Display the resulting image
dog_image.show()
