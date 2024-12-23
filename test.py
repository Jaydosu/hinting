from PIL import Image, ImageDraw

def create_subpixel_rendered_image(size):
    """
    Creates a simulated subpixel-rendered image of a white square (size x size)
    with a black diagonal line.
    """
    # Original image size (100 x 100 pixels)
    original_size = size
    # Subpixel image size (300 x 100, where 1 pixel = 3 subpixels horizontally)
    subpixel_size = (original_size * 3, original_size)
    
    # Create a new white image for subpixel rendering
    img = Image.new("RGB", subpixel_size, "white")
    draw = ImageDraw.Draw(img)

    # Draw the diagonal line using subpixel adjustments
    for y in range(original_size):
        # Map the original pixel to subpixel space
        x_original = y
        x_subpixel = x_original * 3

        # Simulate subpixel darkening for smoothing the diagonal line
        draw.point((x_subpixel, y), fill=(255, 0, 0))  # Darken red subpixel
        draw.point((x_subpixel + 1, y), fill=(0, 0, 0))    # Fully darken (black pixel center)
        draw.point((x_subpixel + 2, y), fill=(0, 0, 255))  # Darken blue subpixel

    return img

# Create and save the subpixel-rendered image
size = 100
image = create_subpixel_rendered_image(size)
image.show()  # Display the image
