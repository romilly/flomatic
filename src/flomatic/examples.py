"""
Examples for the Flomatic code_to_mermaid module.

This file contains example code snippets and functions to demonstrate
the usage of the FlowchartGenerator class for creating Mermaid flowcharts
from Python code.
"""

import os
from flomatic.code_to_mermaid import FlowchartGenerator

# Example code snippets
SOURCE_CODE = '''
def example(x):
    if x > 0:
        return x
    else:
        return -x
'''

FOR_LOOP_CODE = '''
def process_list(items):
    result = 0
    for item in items:
        if item > 0:
            result += item
        else:
            result -= item
    return result
'''

BREAK_CONTINUE_CODE = '''
def find_and_process(items, target):
    result = 0
    found = False
    for item in items:
        if item == target:
            found = True
            break
        if item < 0:
            continue
        result += item
    if found:
        return result
    else:
        return -1
'''

WHILE_LOOP_CODE = '''
def countdown(n):
    while n > 0:
        print(n)
        n -= 1
        if n == 5:
            print("Halfway there!")
    print("Blast off!")

def find_element(data, target):
    i = 0
    while i < len(data):
        if data[i] == target:
            return i
        i += 1
    else:
        return -1
'''

IF_EXAMPLE = """
def example(x):
    if x > 0:
        return x
    else:
        return -x
"""

FOR_EXAMPLE = """
def process_list(items):
    results = []
    for item in items:
        results.append(item * 2)
    return results
"""

BREAK_CONTINUE_EXAMPLE = """
def find_and_process(items, target):
    for i, item in enumerate(items):
        if item == target:
            return i
        if item < 0:
            continue
        print(item)
    return -1
"""

WHILE_EXAMPLE = """
def countdown(n):
    while n > 0:
        print(n)
        n -= 1
        if n == 5:
            print("Five!")
    print("Done!")
    
def find_element(data, target):
    i = 0
    while i < len(data):
        if data[i] == target:
            return i
        i += 1
    else:
        return -1
"""

CLASS_EXAMPLE = """
class Calculator:
    def __init__(self, initial_value=0):
        self.value = initial_value
        
    def add(self, x):
        self.value += x
        return self.value
        
    def subtract(self, x):
        self.value -= x
        return self.value
        
    def multiply(self, x):
        if x == 0:
            return 0
        self.value *= x
        return self.value
"""

def save_example_diagrams():
    """
    Save example Mermaid diagrams to files.
    Creates diagrams for various code examples and saves them to the mermaid_diagrams directory.
    """
    print("Saving diagrams to files...")
    
    # Create output directory for diagrams
    output_dir = "mermaid_diagrams"
    os.makedirs(output_dir, exist_ok=True)
    
    # Example with if statement
    generator = FlowchartGenerator()
    files = generator.save_mermaid_diagram(IF_EXAMPLE, output_dir, compact=True)
    print(f"If statement diagram saved to: {', '.join(files)} (compact mode)")
    
    # Example with for loop
    generator = FlowchartGenerator()
    files = generator.save_mermaid_diagram(FOR_EXAMPLE, output_dir, compact=True)
    print(f"For loop diagram saved to: {', '.join(files)} (compact mode)")
    
    # Example with break and continue
    generator = FlowchartGenerator()
    files = generator.save_mermaid_diagram(BREAK_CONTINUE_EXAMPLE, output_dir, compact=True)
    print(f"Break/continue diagram saved to: {', '.join(files)} (compact mode)")
    
    # Example with while loop
    generator = FlowchartGenerator()
    files = generator.save_mermaid_diagram(WHILE_EXAMPLE, output_dir, compact=True)
    print(f"While loop diagram saved to: {', '.join(files)} (compact mode)")
    
    # Example with class definition
    generator = FlowchartGenerator()
    files = generator.save_mermaid_diagram(CLASS_EXAMPLE, output_dir, compact=True)
    print(f"Class diagram saved to: {', '.join(files)} (compact mode)")
    
    # Example with detailed mode (non-compact)
    detailed_output_dir = "mermaid_diagrams/detailed"
    os.makedirs(detailed_output_dir, exist_ok=True)
    generator = FlowchartGenerator()
    files = generator.save_mermaid_diagram(CLASS_EXAMPLE, detailed_output_dir, compact=False)
    print(f"\nDetailed class diagram saved to: {detailed_output_dir} (full mode)")

def print_example_diagrams():
    """
    Print example Mermaid diagrams to the console.
    Generates and prints diagrams for various code examples.
    """
    # Create a new generator for each example to avoid mixing flowcharts
    if_generator = FlowchartGenerator()
    print("Example with if statement:\n")
    print(if_generator.generate_mermaid_flowchart(SOURCE_CODE))
    
    # Create a new generator for the for loop example
    for_generator = FlowchartGenerator()
    print("\n\nExample with for loop:\n")
    print(for_generator.generate_mermaid_flowchart(FOR_LOOP_CODE))
    
    # Create a new generator for the break and continue example
    break_continue_generator = FlowchartGenerator()
    print("\n\nExample with break and continue:\n")
    print(break_continue_generator.generate_mermaid_flowchart(BREAK_CONTINUE_CODE))
    
    # Create a new generator for the while loop example
    while_generator = FlowchartGenerator()
    print("\n\nExample with while loop:\n")
    print(while_generator.generate_mermaid_flowchart(WHILE_LOOP_CODE))

if __name__ == "__main__":
    # Uncomment one of these lines to choose the behavior
    save_example_diagrams()  # Save diagrams to files
    # print_example_diagrams()  # Print diagrams to console
