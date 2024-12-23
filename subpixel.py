"""
Take an input image, if its color, convert it to grayscale, create an enlarged downscaled appearance of the image with subpixel hinting.



"""
import sys
import os
import numpy as np
from PIL import Image

def subpixel(path, blocksize=20):
  """
  Take an image, convert it to grayscale, create an enlarged downscaled appearance of the image with subpixel hinting. 
  Subpixel rendering: https://www.grc.com/ctwhat.htm

  Args:
    path: str, path to the image file.
    blocksize: int, size of the block (in number of pixels) to be used for subpixel hinting. Default is 20.

  Returns:
    subpixelfied: str, path to the subpixelfied image file. 
  """
  with open(path, "rb") as f:
    img = Image.open(f)
    img = img.convert("L")

  # Get image dimensions
  w, h = img.size

  # Triple the horizontal resolution to simulate subpixel rendering
  img = img.resize((w, h), Image.NEAREST)
  new_w = w * 3

  print(f"Image size: {w}x{h}, Subpixelfied image size: {new_w}x{h}")

  # Divide the image into blocks
  block_w = w // blocksize
  block_h = h // blocksize

  # Create a new image with the same dimensions as the original image
  subpixelfied = Image.new("YCbCr", (w, h))

  # For each block, find the average pixel value and fill the block with that value
  for i in range(block_w):
    for j in range(block_h):
      block = img.crop((i * blocksize, j * blocksize, (i + 1) * blocksize, (j + 1) * blocksize))
      block_avg = int(np.mean(np.array(block)))

      # Get the average of all the pixels in a [+1, (j-1, j+1)] range of the block (i.e. the three blocks to the right of the current block)
      block_right_up = img.crop(((i + 1) * blocksize, (j - 1) * blocksize, (i + 2) * blocksize, j * blocksize))
      block_right = img.crop(((i + 1) * blocksize, j * blocksize, (i + 2) * blocksize, (j + 1) * blocksize))
      block_right_down = img.crop(((i + 1) * blocksize, (j + 1) * blocksize, (i + 2) * blocksize, (j + 2) * blocksize))
      block_right_avg = int(np.mean(np.array(block_right_up) + np.array(block_right) + np.array(block_right_down)))
      
      block_left_up = img.crop(((i - 1) * blocksize, (j - 1) * blocksize, i * blocksize, j * blocksize))
      block_left = img.crop(((i - 1) * blocksize, j * blocksize, i * blocksize, (j + 1) * blocksize))
      block_left_down = img.crop(((i - 1) * blocksize, (j + 1) * blocksize, i * blocksize, (j + 2) * blocksize))
      block_left_avg = int(np.mean(np.array(block_left_up) + np.array(block_left) + np.array(block_left_down)))

      threshhold = 110
      intensity = 1/5
      block_avg_adj = int(block_avg * intensity)

      # If the block to the right is black, paste the red pixel
      if block_right_avg < threshhold and i != block_w - 1:
        subpixelfied.paste((block_avg, 128, 128), (i * blocksize, j * blocksize, (i + 1) * blocksize, (j + 1) * blocksize))

      # If the block to the left is black, paste the blue pixel
      elif block_left_avg < threshhold and i != 0:
        subpixelfied.paste((block_avg_adj, 128, 128), (i * blocksize, j * blocksize, (i + 1) * blocksize, (j + 1) * blocksize))

      else:
        subpixelfied.paste((block_avg, 128, 128), (i * blocksize, j * blocksize, (i + 1) * blocksize, (j + 1) * blocksize))

  # Resize the image to the original dimensions
  subpixelfied = subpixelfied.resize((w, h), Image.NEAREST)

  # Save the subpixelfied image
  subpixelfied_path = os.path.splitext(path)[0] + "_subpixelfied.jpg"
  subpixelfied.save(subpixelfied_path)

  print(f"Subpixelfied image saved at {subpixelfied_path}")
  return subpixelfied_path


if __name__ == "__main__":
  filepath = "work_1200.jpg"
  scale = 10

  subpixelfied = subpixel(filepath, scale)