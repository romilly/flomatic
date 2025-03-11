#!/usr/bin/env python3
"""
Script to generate Mermaid diagrams for the FlowchartGenerator class itself.
"""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from flomatic.code_to_mermaid import FlowchartGenerator

def main():
    # Path to the code_to_mermaid.py file
    source_file = os.path.join('src', 'flomatic', 'code_to_mermaid.py')
    output_dir = 'mermaid_diagrams'
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the source code
    with open(source_file, 'r') as f:
        source_code = f.read()
    
    # Create a FlowchartGenerator instance
    generator = FlowchartGenerator()
    
    # Generate diagrams for all functions in the file
    file_paths = generator.save_mermaid_diagram(source_code, output_dir=output_dir)
    
    print(f"Generated {len(file_paths)} Mermaid diagram files in {output_dir}:")
    for path in file_paths:
        print(f"  - {path}")

if __name__ == "__main__":
    main()
