"""
Goal: take an image file and apply antialiasing to it, and then scale it up to a larger size for visual effect.
Part of a larger project to achieve a aesthetic of a scaled up type-hinted image but with different
colour channels instead of just red and blue.

Inspiration article: https://medium.com/@evanwallace/easy-scalable-text-rendering-on-the-gpu-c3f4d782c5ac
Inspiration image: https://miro.medium.com/v2/resize:fit:720/format:webp/1*tvwUlcG0bKAYq1Wy17_V4Q.png

We can skip most of the steps in the article as we are not rendering text, but we can use the antialiasing technique.
From the article: "the problem is that every pixel is either completely filled in or completely empty" - referring to
the anti-aliasing problem. The solution is to use a technique called "subpixel rendering" which is a form of antialiasing. 

We want to leverage the subpixel rendering aesthetic to create a new image with a similar aesthetic but at a higher resolution.

Constraints of the project:

- The image must be black and white (greyscale) to start with.
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from matplotlib import pyplot as plt

def antialias(image_path, downsample_factor=20):
    """
    After the first attempt we need to have a higher resolution image as the input, then downsample it before applying antialiasing.

    For example taking a 400x400 image and downsampling it to maybe 20x20, then applying antialiasing, then scaling it back up to 400x400.
    """
    # Open an image file

    # get original image size
    original_img_size = Image.open(image_path).size
    
    downsampled_img_size = (original_img_size[0] // downsample_factor, original_img_size[1] // downsample_factor)

    with Image.open(image_path) as img:
        # Downsample the image

        img = img.resize(downsampled_img_size, Image.Resampling.HAMMING)
        img = img.resize(original_img_size, Image.Resampling.NEAREST)

    return img

def subpixel_aa(image_path, downsample_factor=20):
    """
    Take an already antialiased image and apply subpixel rendering to it.

    Subpixel rendering involves splitting each pixel into 3 subpixels, one for red, green, and blue.
    This is to simulate the effect of an LCD screen where each pixel is made up of 3 subpixels.

    """
    # perform subpixel anti-aliasing
    with Image.open(image_path) as img:
        # get original image size
        original_img_size = img.size
        print(img.size)

        # upscale the image 3x in width for subpixel rendering to the nearest number of downsample factor
        nearest_width = 3* original_img_size[0] + (downsample_factor - (3*original_img_size[0]) % downsample_factor)
        nearest_height = 3* original_img_size[1] + (downsample_factor - (3*original_img_size[1]) % downsample_factor)
        subpixel_img = img.resize((nearest_width, nearest_height), Image.Resampling.NEAREST)
        print(subpixel_img.size)


        # Create a new image with the same size as the original
        new_img = Image.new("RGB", subpixel_img.size)

        # For each pixel in the image get the black and white value and then colour the subpixels accordingly
        # Split each pixel into 3 subpixels, one for red, green, and blue
        r, g, b = subpixel_img.split()

        # Greyscale intensity formula
        # I = 0.2989*R + 0.5870*G + 0.1140*B
        # We can use this formula to get the intensity of the pixel and then use it to colour the subpixels
        GI = lambda r, g, b: int(0.2989*r + 0.587*g + 0.114*b)

        # iterate over the downsample factor number of columns multiplied by 3 but the rows is just the downsample factor
        for column in range(0, subpixel_img.size[0], downsample_factor):
            for row in range(0, subpixel_img.size[1], downsample_factor):
                # Get the pixel value
                pixel = subpixel_img.getpixel((column, row))
                
                # Get the intensity of the pixel
                intensity = GI(*pixel)
                # Colour the area of subpixels 
                draw = ImageDraw.Draw(new_img)
                # Red subpixel
                if intensity < 250:
                    if column // downsample_factor % 3 == 0:
                        draw.rectangle([column, row, column + downsample_factor, row + downsample_factor], fill=(intensity, 0, 0))
                    # Green subpixel
                    if column // downsample_factor % 3 == 1:
                        draw.rectangle([column, row, column + downsample_factor, row + downsample_factor], fill=(0, intensity, 0))
                    # Blue subpixel
                    if column // downsample_factor % 3 == 2:
                        draw.rectangle([column, row, column + downsample_factor, row + downsample_factor], fill=(0, 0, intensity))
                else:
                    draw.rectangle([column, row, column + downsample_factor, row + downsample_factor], fill=(255, 255, 255))

        # turn the image in to greyscale
        #new_img = new_img.convert("L")

        # stack the original image resized to the new image size on top of the new image
        newer_img = Image.new("RGB", (new_img.size[0], new_img.size[1] * 2))
        img = img.resize(new_img.size, Image.Resampling.NEAREST)
        newer_img.paste(img, (0, 0))
        newer_img.paste(new_img, (0, new_img.size[1]))

        new_img = newer_img
        


            
    return new_img


if __name__ == "__main__":
    antialiased_img = antialias(os.getcwd() + "\\hinting\\working\\rsgt.jpg", 10)
    antialiased_img.save(os.getcwd() + "\\hinting\\working\\output\\antialiased.jpg")

    subpixel_img = subpixel_aa(os.getcwd() + "\\hinting\\working\\output\\antialiased.jpg")
    #subpixel_img = subpixel_aa(os.getcwd() + "\\hinting\\working\\rsgt.jpg", 20)
    subpixel_img.save(os.getcwd() + "\\hinting\\working\\output\\subpixel.jpg")