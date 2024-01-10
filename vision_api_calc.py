import argparse
from PIL import Image


def calculate_cost_from_dimensions(width, height, detail_level):
    """
    Calculate the token cost based on the given dimensions and detail level.

    :param width: Width of the image
    :param height: Height of the image
    :param detail_level: 'high' or 'low'
    :return: Token cost
    """
    if detail_level == 'low':
        return 85  # Fixed cost for low detail images

    # For high detail images
    # Step 1: Scale to fit within a 2048 x 2048 square
    if width > 2048 or height > 2048:
        aspect_ratio = width / height
        if width > height:
            width = 2048
            height = int(width / aspect_ratio)
        else:
            height = 2048
            width = int(height * aspect_ratio)

    # Step 2: Scale such that the shortest side is 768px
    if width < height:
        scale_factor = 768 / width
    else:
        scale_factor = 768 / height
    width = int(width * scale_factor)
    height = int(height * scale_factor)

    # Step 3: Count 512px squares
    # squares_count = (width // 512) * (height // 512)
    squares_count = ((width + 511) // 512) * ((height + 511) // 512)

    # Step 4: Calculate cost
    return 170 * squares_count + 85


def calculate_token_cost(image_file=None, width=None, height=None, detail_level='low'):
    """
    Calculate the token cost based on an image file or given dimensions.

    :param image_file: Path to the image file (optional)
    :param width: Width of the image (optional)
    :param height: Height of the image (optional)
    :param detail_level: 'high' or 'low'
    :return: Token cost
    """
    if image_file:
        with Image.open(image_file) as img:
            width, height = img.size

    if width is not None and height is not None:
        return calculate_cost_from_dimensions(width, height, detail_level)

    raise ValueError("Either image_file or both width and height must be provided")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate token cost based on image dimensions.')
    parser.add_argument('--image', help='Path to the image file')
    parser.add_argument('--width', type=int, help='Width of the image')
    parser.add_argument('--height', type=int, help='Height of the image')
    parser.add_argument('--detail-level', choices=['low', 'high'], default='high', help='Detail level (low or high)')

    args = parser.parse_args()

    try:
        token_cost = calculate_token_cost(image_file=args.image, width=args.width, height=args.height, detail_level=args.detail_level)
        print(token_cost)
    except ValueError as e:
        print(f'Error: {str(e)}')