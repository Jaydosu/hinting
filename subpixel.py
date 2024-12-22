"""
Take an input image, if its color, convert it to grayscale, create an enlarged downscaled appearance of the image with subpixel hinting.



"""
import sys
import os
import numpy as np
from PIL import Image

def subpixel(path, scale):
  """
  Take an image, convert it to grayscale, create an enlarged downscaled appearance of the image with subpixel hinting. 
  Subpixel rendering: https://www.grc.com/ctwhat.htm

  Args:
    path: str, path to the image file.
    scale: int, the scale factor to downscale the image by. Default is 4. The downscaling will try to find a downscaled size which
    is the largest possible integer factor of the original image size. For example, if the original image is 100x100, and the scale
    is 4, the downscale size will be 25x25. If the scale is 3, the downscale size will be 33x33.

  Returns:
    subpixelfied: str, path to the subpixelfied image file. 
  """
  with open(path, "rb") as f:
    img = Image.open(f)
    img = img.convert("L")

  # Get image dimensions
  w, h = img.size

  # Find the scaled dimensions. Apply a further division by 3 to find the subpixel widths.
  # If the dimensions cannot be scaled, return an error
  w_scaled = w // scale
  h_scaled = h // scale

  width_column_size = w_scaled % 3

  print(f"original image dimensions: {h}x{w}")
  print(f"New image dimensions: {h_scaled}x{w_scaled}")

  img = img.resize((w_scaled, h_scaled), Image.BOX)
  
  if w_scaled == 0 or h_scaled == 0:
    return "Cannot scale image"

  output_name = path.split(".")[0] + "_subpixelfied." + path.split(".")[1]
  img.save(output_name)
  print(f"Image saved as {output_name}")
  return output_name


if __name__ == "__main__":
  filepath = "work_1200.jpg"
  scale = 4

  subpixelfied = subpixel(filepath, scale)