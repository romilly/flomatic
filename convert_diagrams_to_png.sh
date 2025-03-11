#!/bin/bash
# Script to convert all Mermaid diagram files (.mmd) to PNG format

# Create output directory if it doesn't exist
mkdir -p mermaid_diagrams/png

# Convert each .mmd file to PNG
for file in mermaid_diagrams/*.mmd; do
    filename=$(basename "$file" .mmd)
    echo "Converting $filename.mmd to PNG..."
    mmdc -i "$file" -o "mermaid_diagrams/png/$filename.png"
done

echo "Conversion complete. PNG files are in mermaid_diagrams/png directory."
