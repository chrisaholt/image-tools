# Code from ChatGPT on 06/15/24

### Example usage
# png_path = "path_to_your_png_file.png"
# svg_path = "output_svg_file.svg"
# png_to_svg(png_path, svg_path)

import argparse
import cv2
import numpy as np
import svgwrite
from svgwrite import mm

def convert_image_with_transparency_to_grayscale(img_4_channel):
    pass

def png_to_svg(png_path, svg_path):
    # Load the image, with alpha channel as mask.
    img = cv2.imread(png_path, cv2.IMREAD_UNCHANGED)
    img = np.clip(img[:, :, 3], 0, 255)

    # Threshold binary mask.
    thresh = 127
    white_coords = (img > thresh)
    black_coords = (img <= thresh)
    img[black_coords] = 255
    img[white_coords] = 0

    # Check if image is loaded
    if img is None:
        print("Error: Image could not be read.")
        return

    # Convert to binary (black and white)
    _, threshold = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create SVG drawing
    dwg = svgwrite.Drawing(svg_path, profile="tiny", size=(img.shape[1] * mm, img.shape[0] * mm))

    # Draw contours
    for contour in contours:
        # Convert contour points to a format suitable for svgwrite
        points = [(str(point[0][0]), str(point[0][1])) for point in contour]
        # Add polygon to the drawing
        polygon_points = dwg.polygon(points)
        dwg.add(polygon_points)

    # Save SVG file
    dwg.save()
    print(f"SVG file created at {svg_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert binary PNG to SVG.")
    parser.add_argument("png_path", type=str, help="Path to the PNG file to convert.")
    parser.add_argument("svg_path", type=str, help="Path to the ouput SVG file.")
    args = parser.parse_args()
    png_to_svg(args.png_path, args.svg_path)