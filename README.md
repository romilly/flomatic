# Flomatic

Flomatic is a Python tool that automatically generates Mermaid flowcharts from Python source code. It helps developers visualize the control flow of their code by creating diagrams that represent functions, loops, conditionals, and other control structures.

## Features

- Generate Mermaid flowcharts from Python source code
- Visualize control flow structures including:
  - Functions and methods
  - If/else statements
  - For loops
  - While loops
  - Break and continue statements
  - Return statements
  - Class definitions
- Terminal nodes (like return statements) are properly connected to the End node
- Target specific functions or methods for visualization
- Choose between compact mode (control flow only) or detailed mode (all AST nodes)
- Save diagrams to files or output to console

## Installation

Flomatic requires Python 3.8+ and the standard library modules `ast`, `os`, and `re`.

To set up the project with the included virtual environment:

```bash
# Activate the virtual environment
source venv/bin/activate
```

## Usage

### Basic Example

```python
from flomatic.code_to_mermaid import FlowchartGenerator

# Create a generator
generator = FlowchartGenerator()

# Example Python code
source_code = '''
def example(x):
    if x > 0:
        return x
    else:
        return -x
'''

# Generate a Mermaid flowchart as a string
flowchart = generator.generate_mermaid_flowchart(source_code)
print(flowchart)

# Or save the flowchart to a file
output_files = generator.save_mermaid_diagram(source_code, output_dir="mermaid_diagrams")
```

### Using the Examples Module

Flomatic includes an examples module with pre-defined code snippets and functions to demonstrate usage:

```python
# Import the examples module
from flomatic import examples

# Generate and save example diagrams to the mermaid_diagrams directory
examples.save_example_diagrams()

# Or print example diagrams to the console
examples.print_example_diagrams()
```

### Options

- **Target specific functions**: Generate a flowchart for a specific function by providing its name
  ```python
  flowchart = generator.generate_mermaid_flowchart(source_code, target_function="example")
  ```

- **Class methods**: Target methods within classes using dot notation
  ```python
  flowchart = generator.generate_mermaid_flowchart(source_code, target_function="Calculator.multiply")
  ```

- **Detailed mode**: Include all AST nodes in the diagram (not just control flow)
  ```python
  flowchart = generator.generate_mermaid_flowchart(source_code, compact=False)
  ```

## Output

Flomatic generates Mermaid flowchart syntax, which can be rendered by any Mermaid-compatible tool. The output files have the `.mmd` extension.

Example output for a simple function:

```
flowchart TD
Start["Start"]
node1["Function example"]
Start --> node1
node2["If: x > 0"]
node1 --> node2
node3["Then"]
node2 --> node3
node4["Return: x"]
node3 --> node4
node5["Else"]
node2 --> node5
node6["Return: -x"]
node5 --> node6
End["End"]
node4 --> End
node6 --> End
```

Note how all terminal nodes (like return statements) are properly connected to the End node, making the flow of execution clear.

## Viewing the Diagrams

You can view the generated Mermaid diagrams using:

1. Mermaid Live Editor: https://mermaid.live/
2. VS Code with a Mermaid extension
3. GitHub (which natively supports Mermaid in markdown)
4. Any other tool that supports Mermaid syntax

## Converting Diagrams to Images

Flomatic generates Mermaid syntax files (`.mmd`), which can be converted to image formats like PNG or SVG using the Mermaid CLI tool.

### Installing Mermaid CLI

The Mermaid CLI requires Node.js and npm. To install:

```bash
# Install Node.js and npm if you don't have them already
# Then install the Mermaid CLI globally
npm install -g @mermaid-js/mermaid-cli
```

### Converting .mmd Files to Images

Once you have the Mermaid CLI installed, you can convert your `.mmd` files to images:

```bash
# Convert a single file to PNG
mmdc -i path/to/diagram.mmd -o output.png

# Convert a single file to SVG
mmdc -i path/to/diagram.mmd -o output.svg

# Convert all .mmd files in a directory to PNG
for file in mermaid_diagrams/*.mmd; do
    mmdc -i "$file" -o "${file%.mmd}.png"
done
```

### Customizing Output

You can customize the output with various options:

```bash
# Set background color
mmdc -i diagram.mmd -o output.png -b transparent

# Set custom width and height
mmdc -i diagram.mmd -o output.png -w 1024 -h 768

# Use a custom CSS file
mmdc -i diagram.mmd -o output.png -c custom.css
```

For more options, run `mmdc --help` or refer to the [Mermaid CLI documentation](https://github.com/mermaid-js/mermaid-cli).

## Development

### Project Structure

```
flomatic/
├── src/
│   └── flomatic/
│       ├── __init__.py
│       ├── code_to_mermaid.py  # Core functionality
│       └── examples.py         # Example code and usage
├── tests/                      # Test suite
│   ├── test_flowchart_generator.py
│   ├── test_examples.py
│   ├── test_import.py
│   └── conftest.py
├── mermaid_diagrams/           # Generated diagrams (when run)
├── generate_self_diagrams.py   # Script to generate diagrams for the codebase itself
├── venv/                       # Virtual environment
├── pytest.ini                  # Pytest configuration
├── LICENSE                     # MIT License
└── README.md                   # This file
```

### Running Tests

Flomatic includes a comprehensive test suite using pytest. To run the tests:

```bash
# Activate the virtual environment
source venv/bin/activate

# Install pytest if not already installed
pip install pytest

# Run the tests
python -m pytest
```

### Generating Diagrams for the Codebase

Flomatic includes a script to generate flowcharts for its own codebase, which serves as both a demonstration and a form of self-documentation:

```bash
# Run the script to generate diagrams for the FlowchartGenerator class
python generate_self_diagrams.py
```

This will create Mermaid diagram files in the `mermaid_diagrams` directory, one for each method in the FlowchartGenerator class. These diagrams provide a visual representation of how the code works, making it easier to understand and maintain.

## License

Flomatic is released under the MIT License.

```
MIT License

Copyright (c) 2025 Romilly Cocking

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

See the [LICENSE](LICENSE) file for the full license text.
