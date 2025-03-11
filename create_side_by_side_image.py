#!/usr/bin/env python3
"""
Script to create a side-by-side image with source code and flowchart.
"""

import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

def extract_function_source(file_path, function_name):
    """Extract the source code for a specific function from a file."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    function_lines = []
    in_function = False
    indent_level = 0
    
    for line in lines:
        if f"def {function_name}" in line:
            in_function = True
            indent_level = len(line) - len(line.lstrip())
            function_lines.append(line)
        elif in_function:
            # Check if we've exited the function (less indentation)
            if line.strip() and len(line) - len(line.lstrip()) <= indent_level and not line.strip().startswith(('#', '"""', "'''", '@')):
                break
            function_lines.append(line)
    
    return ''.join(function_lines)

def create_side_by_side_image(source_code, flowchart_path, output_path, width=1920, height=1080):
    """Create a side-by-side image with source code and flowchart."""
    # Create a new image with white background
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Try to load a nice monospace font, fall back to default if not available
    try:
        code_font = ImageFont.truetype("DejaVuSansMono.ttf", 14)
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)
    except IOError:
        code_font = ImageFont.load_default()
        title_font = ImageFont.load_default()
    
    # Draw title for source code
    draw.text((20, 20), "Source Code: generate_mermaid_flowchart", fill='black', font=title_font)
    
    # Draw source code
    wrapped_code = []
    for line in source_code.split('\n'):
        wrapped_code.append(line)
    
    y_position = 60
    for line in wrapped_code:
        draw.text((20, y_position), line, fill='black', font=code_font)
        y_position += 20
    
    # Load and resize flowchart image
    flowchart_image = Image.open(flowchart_path)
    
    # Calculate the right side width
    right_width = width // 2
    
    # Calculate the aspect ratio to maintain proportions
    aspect_ratio = flowchart_image.width / flowchart_image.height
    right_height = int(right_width / aspect_ratio)
    
    # If the height is too large, scale based on height instead
    if right_height > height - 40:
        right_height = height - 40
        right_width = int(right_height * aspect_ratio)
    
    # Resize the flowchart image
    flowchart_image = flowchart_image.resize((right_width, right_height))
    
    # Calculate position to center the flowchart on the right side
    right_x = width // 2 + (width // 2 - right_width) // 2
    right_y = (height - right_height) // 2
    
    # Draw title for flowchart
    draw.text((width // 2 + 20, 20), "Flowchart Diagram", fill='black', font=title_font)
    
    # Paste the flowchart image
    image.paste(flowchart_image, (right_x, right_y))
    
    # Draw a vertical line to separate the two sides
    draw.line([(width // 2, 0), (width // 2, height)], fill='black', width=2)
    
    # Save the image
    image.save(output_path)
    print(f"Image saved to {output_path}")

if __name__ == "__main__":
    # Paths
    code_file = "src/flomatic/code_to_mermaid.py"
    flowchart_png = "mermaid_diagrams/png/FlowchartGenerator.generate_mermaid_flowchart.png"
    output_file = "side_by_side.png"
    
    # Extract source code
    source_code = extract_function_source(code_file, "generate_mermaid_flowchart")
    
    # Create the side-by-side image
    create_side_by_side_image(source_code, flowchart_png, output_file)
