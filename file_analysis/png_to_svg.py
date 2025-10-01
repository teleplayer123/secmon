from PIL import Image
import numpy as np
import potrace
import sys

def png_to_svg(png_path, svg_path):
    # Load image and convert to black and white
    image = Image.open(png_path).convert("L")
    bw = image.point(lambda x: 0 if x < 128 else 1, '1')

    # Convert to numpy array
    bitmap_array = np.array(bw, dtype=np.uint8)

    # Create potrace bitmap
    bmp = potrace.Bitmap(bitmap_array)
    path = bmp.trace()

    # Write to SVG
    with open(svg_path, 'w') as f:
        f.write('<?xml version="1.0" standalone="no"?>\n')
        f.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.0//EN"\n')
        f.write('"http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
        f.write('<svg xmlns="http://www.w3.org/2000/svg" version="1.0">\n')
        for curve in path:
            f.write('<path d="')
            for segment in curve:
                if segment.is_corner:
                    f.write(f'L {segment.c[1][0]} {segment.c[1][1]} ')
                else:
                    f.write(f'C {segment.c[0][0]} {segment.c[0][1]}, {segment.c[1][0]} {segment.c[1][1]}, {segment.c[2][0]} {segment.c[2][1]} ')
            f.write('" fill="black"/>\n')
        f.write('</svg>\n')

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python png_to_svg.py input.png output.svg")
    else:
        png_to_svg(sys.argv[1], sys.argv[2])