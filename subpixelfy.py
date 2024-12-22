"""
Take an input image, if its color, convert it to grayscale, create an enlarged downscaled appearance of the image with subpixel hinting.



"""

import sys
import os
import numpy as np
from PIL import Image

def subpixelfy(image, scale=4):
  """
  Take an image, convert it to grayscale, create an enlarged downscaled appearance of the image with subpixel hinting. 
  Subpixel rendering: https://www.grc.com/ctwhat.htm

  It is a technique used in LCD screens to increase the resolution of the display by using the three subpixels
  in each pixel to display different colors.
  We would like to replicate the effect of subpixel rendering in a grayscale image, but we would like to then 
  upscale the image to make it appear as if it was rendered at a higher resolution, while keeping the low 
  resolution effect.

  Args:
    image: str, path to the image file.
    scale: int, the scale factor to downscale the image by. Default is 4. The downscaling will try to find a downscaled size which
    is the largest possible integer factor of the original image size. For example, if the original image is 100x100, and the scale
    is 4, the downscale size will be 25x25. If the scale is 3, the downscale size will be 33x33.

  Returns:
    subpixelfied: str, path to the subpixelfied image file.
  """
  # Get image name
  imgname = image.split('.')[0]
  output_name = imgname + '_subpixelfied.' + image.split('.')[1]

  # Load the image and keep ONLY the black pixels
  img = Image.open(image)

  # get image dimensions
  w, h = img.size
  print(f"Image dimensions: {h}x{w}")

  # Find the dimensions of the downscaled image
  downscale_w = w // scale
  downscale_h = h // scale

  # Starting from 0 on the x axis, go horizontally until we find the first black pixel
  # Then, starting from the last pixel on the x axis, go backwards until we find the last black pixel
  # This will give us the horizontal range of the black pixels

  # Convert image to grayscale
  img = img.convert('L')

  # Convert image to numpy array
  img_array = np.array(img)

  # Find the first black pixel in each column
  first_black_pixel = None
  last_black_pixel = None
  for x in range(w):
    for y in range(h):
      if img_array[y, x] == 0:  # 0 indicates black in grayscale
        first_black_pixel = x
        break
    if first_black_pixel:
      break

  # Find the last black pixel in each column
  for x in range(w - 1, -1, -1):
    for y in range(h):
      if img_array[y, x] == 0:  # 0 indicates black in grayscale
        last_black_pixel = x
        break
    if last_black_pixel:
      break

  print(f"First black pixel found at: {first_black_pixel}")
  print(f"Last black pixel found at: {last_black_pixel}")

  black_width = last_black_pixel - first_black_pixel # Width of the black pixels, we want to align this to the subpixels

  # Increase horizontal resolution by 3x, and vertical resolution by 1x to simulate subpixel rendering
  # We'll also crop the image to the width of the black pixels
  cropped_img = img.crop((first_black_pixel, 0, last_black_pixel + 1, h))

  # Downscale to achieve a downscaled appearance
  cropped_img = cropped_img.resize((w // scale, h // scale), Image.NEAREST)

  # Upscale the cropped image by 3x horizontally and 1x vertically
  subpixelfied_w = black_width * 3
  subpixelfied_h = h
  subpixelfied_img = cropped_img.resize((subpixelfied_w, subpixelfied_h), Image.NEAREST).convert('RGB')

  # Subpixel rendering
  # do just the red channel for now. since we downscaled by 4, we can iterate over groups of 4 pixels.
  # the first pixel will be the red pixel, the second will be the green pixel, and the third will be the blue pixel.
  # we'll set the green and blue pixels to 0, and the red pixel to the value of the original pixel.
  subpixelfied_array = np.array(subpixelfied_img)
  for x in np.arange(0, subpixelfied_w, 3*scale):
    for y in range(subpixelfied_h):
      subpixelfied_array[y, x:x+4] = (255, 0, 0)
      #subpixelfied_array[y, x+5:x+9] = (0, 255, 0) # green pixel
      #subpixelfied_array[y, x+10:x+14] = (0, 0, 255) # blue pixel

  # Convert the numpy array back to an image
  subpixelfied_img = Image.fromarray(subpixelfied_array)

  
  
  # Temp just save the image
  img = subpixelfied_img
  img.save(output_name)
  print(f"Subpixelfied image dimensions: {subpixelfied_h}x{subpixelfied_w}")
  print(f"Subpixelfied image saved as {output_name}")
  
  

def compare(image):
  """
  make a comparison between the original image and the subpixelfied image.
  """

  # Load the original and subpixelfied images
  original = Image.open(image)
  subpixelfied_name = image.split('.')[0] + '_subpixelfied.' + image.split('.')[1]
  subpixelfied = Image.open(subpixelfied_name)

  # Create a new image with double the width of the original image to place them side by side
  comparison = Image.new('RGB', (original.width + subpixelfied.width, original.height))

  # Paste the original and subpixelfied images into the new image
  comparison.paste(original, (0, 0))
  comparison.paste(subpixelfied, (original.width, 0))

  # Save the comparison image
  comparison_name = image.split('.')[0] + '_comparison.' + image.split('.')[1]
  comparison.save(comparison_name)

  print(f"Comparison image saved as {comparison_name}")

if __name__ == "__main__":
  image = os.getcwd() + "//rsgt_og.jpg"
  subpixelfied = subpixelfy(image)
  comparison = compare(image)