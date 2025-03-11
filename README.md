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
```

## Viewing the Diagrams

You can view the generated Mermaid diagrams using:

1. Mermaid Live Editor: https://mermaid.live/
2. VS Code with a Mermaid extension
3. GitHub (which natively supports Mermaid in markdown)
4. Any other tool that supports Mermaid syntax

## License

[Add license information here]
