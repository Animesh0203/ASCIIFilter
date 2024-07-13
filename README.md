# ASCIICORE Functions

This Streamlit app, ASCIICORE, provides several image processing functions to manipulate and convert images into ASCII art.

## Functions and Parameters

### `resize_if_necessary(image)`

Resizes an image if its total pixel count exceeds a predefined limit.

- **Parameters:**
  - `image`: PIL.Image - The input image to resize if necessary.

### `downscale_image(img, pixel_size)`

Downscales an image by averaging pixels over a specified size.

- **Parameters:**
  - `img`: PIL.Image - The input image to be downscaled.
  - `pixel_size`: int - Size to downscale the image by.

### `quantize_image(img, n=10)`

Quantizes the luminance levels of an image to a specified number.

- **Parameters:**
  - `img`: PIL.Image - The input image to be quantized.
  - `n`: int (default 10) - Number of quantization levels.

### `create_ascii_image(img, ascii_chars=' .:-=+*#%■', char_image_dir='8_Lumi')`

Converts an image into ASCII art using custom characters.

- **Parameters:**
  - `img`: PIL.Image - The input image to convert.
  - `ascii_chars`: str - Characters to use for ASCII art representation.
  - `char_image_dir`: str - Directory containing custom character images.

### Folder Structure

```
📦ImageFilter
 ┣ 📂8_Lumi
 ┃ ┣ 📜032.jpg
 ┃ ┣ 📜035.jpg
 ┃ ┣ 📜037.jpg
 ┃ ┣ 📜042.jpg
 ┃ ┣ 📜043.jpg
 ┃ ┣ 📜045.jpg
 ┃ ┣ 📜046.jpg
 ┃ ┣ 📜058.jpg
 ┃ ┣ 📜061.jpg
 ┃ ┣ 📜064.jpg
 ┃ ┗ 📜9632.jpg
 ┣ 📜app.py
 ┣ 📜ASCII.py
 ┣ 📜Bloom.py
 ┣ 📜Contrast.py
 ┣ 📜DiffOfGaus.py
 ┣ 📜dog_image.jpg
 ┣ 📜Downscale.py
 ┣ 📜GeneratePixelLetters.py
 ┣ 📜main.py
 ┣ 📜ModifiedPixelArr.py
 ┣ 📜pexels-lumn-406014.jpg
 ┣ 📜ReplacePixels.py
 ┣ 📜ScaleLuminance.py
 ┣ 📜SobelColorEdges.py
 ┣ 📜SobelFilter(CUDA).py
 ┣ 📜SobelFilter.py
 ┣ 📜sobel_output.jpg
 ┣ 📜sobel_output_color_edges.jpg
 ┣ 📜sobel_output_cuda.jpg
 ┣ 📜sobel_output_high_threshold.jpg
 ┗ 📜sobel_output_thresholded.jpg
```
