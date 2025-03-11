"""
Unit tests for the FlowchartGenerator class.
"""

import os
import pytest
from flomatic.code_to_mermaid import FlowchartGenerator

# Test code snippets
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


class TestFlowchartGenerator:
    """Test cases for the FlowchartGenerator class."""

    def test_initialization(self):
        """Test that the FlowchartGenerator initializes correctly."""
        generator = FlowchartGenerator()
        assert generator.flowchart == ["flowchart TD"]
        assert generator.node_count == 0
        assert generator.last_node == "Start"
        assert generator.loop_start_node is None
        assert generator.after_loop_node is None

    def test_add_node(self):
        """Test that add_node creates a node with the correct label."""
        generator = FlowchartGenerator()
        node_name = generator.add_node("Test Node")
        assert node_name == "node1"
        assert generator.node_count == 1
        assert generator.flowchart[1] == 'node1["Test Node"]'

    def test_add_connection(self):
        """Test that add_connection creates a connection between nodes."""
        generator = FlowchartGenerator()
        generator.add_connection("nodeA", "nodeB")
        assert generator.flowchart[1] == "nodeA --> nodeB"

    def test_generate_if_statement_flowchart(self):
        """Test generating a flowchart for code with an if statement."""
        generator = FlowchartGenerator()
        flowchart = generator.generate_mermaid_flowchart(IF_EXAMPLE)
        
        # Check that the flowchart contains the expected elements
        assert "flowchart TD" in flowchart
        assert "Start" in flowchart
        assert "Function example" in flowchart
        assert "If: x > 0" in flowchart
        assert "Then" in flowchart
        assert "Return: x" in flowchart
        assert "Else" in flowchart
        assert "Return: -x" in flowchart
        assert "End" in flowchart

    def test_generate_for_loop_flowchart(self):
        """Test generating a flowchart for code with a for loop."""
        generator = FlowchartGenerator()
        flowchart = generator.generate_mermaid_flowchart(FOR_EXAMPLE)
        
        # Check that the flowchart contains the expected elements
        assert "flowchart TD" in flowchart
        assert "Start" in flowchart
        assert "Function process_list" in flowchart
        assert "For: " in flowchart and "in items" in flowchart
        assert "Loop Body" in flowchart
        assert "After Loop" in flowchart
        assert "Return: results" in flowchart
        assert "End" in flowchart

    def test_generate_while_loop_flowchart(self):
        """Test generating a flowchart for code with a while loop."""
        generator = FlowchartGenerator()
        flowchart = generator.generate_mermaid_flowchart(WHILE_EXAMPLE)
        
        # Check that the flowchart contains the expected elements
        assert "flowchart TD" in flowchart
        assert "Start" in flowchart
        assert "Function countdown" in flowchart
        assert "While: n > 0" in flowchart
        assert "Loop Body" in flowchart
        assert "After Loop" in flowchart
        assert "End" in flowchart

    def test_generate_break_continue_flowchart(self):
        """Test generating a flowchart for code with break and continue statements."""
        generator = FlowchartGenerator()
        flowchart = generator.generate_mermaid_flowchart(BREAK_CONTINUE_EXAMPLE)
        
        # Check that the flowchart contains the expected elements
        assert "flowchart TD" in flowchart
        assert "Start" in flowchart
        assert "Function find_and_process" in flowchart
        assert "For: " in flowchart and "enumerate(items)" in flowchart
        assert "If: item == target" in flowchart
        assert "Return: i" in flowchart
        assert "If: item < 0" in flowchart
        assert "Continue" in flowchart
        assert "Return: -1" in flowchart
        assert "End" in flowchart

    def test_generate_class_flowchart(self):
        """Test generating a flowchart for code with a class definition."""
        generator = FlowchartGenerator()
        flowchart = generator.generate_mermaid_flowchart(CLASS_EXAMPLE)
        
        # Check that the flowchart contains the expected elements
        assert "flowchart TD" in flowchart
        assert "Start" in flowchart
        assert "Class Calculator" in flowchart
        assert "Function __init__" in flowchart
        assert "Function add" in flowchart
        assert "Function subtract" in flowchart
        assert "Function multiply" in flowchart
        assert "If: x == 0" in flowchart
        assert "Return: 0" in flowchart
        assert "End" in flowchart

    def test_target_specific_function(self):
        """Test generating a flowchart for a specific function in the code."""
        generator = FlowchartGenerator()
        flowchart = generator.generate_mermaid_flowchart(CLASS_EXAMPLE, target_function="Calculator.multiply")
        
        # Check that the flowchart contains only the multiply function
        assert "flowchart TD" in flowchart
        assert "Start" in flowchart
        assert "Function multiply" in flowchart
        assert "If: x == 0" in flowchart
        assert "Return: 0" in flowchart
        assert "End" in flowchart
        
        # Check that other functions are not included
        assert "Function __init__" not in flowchart
        assert "Function add" not in flowchart
        assert "Function subtract" not in flowchart

    def test_compact_vs_detailed_mode(self):
        """Test the difference between compact and detailed mode."""
        # Generate flowchart in compact mode (default)
        compact_generator = FlowchartGenerator()
        compact_flowchart = compact_generator.generate_mermaid_flowchart(IF_EXAMPLE, compact=True)
        
        # Generate flowchart in detailed mode
        detailed_generator = FlowchartGenerator()
        detailed_flowchart = detailed_generator.generate_mermaid_flowchart(IF_EXAMPLE, compact=False)
        
        # Detailed mode should have more nodes than compact mode
        assert len(detailed_flowchart.split("\n")) > len(compact_flowchart.split("\n"))

    @pytest.mark.skipif(not os.path.exists("temp_test_dir"), reason="Requires temp_test_dir to exist")
    def test_save_mermaid_diagram(self):
        """Test saving a Mermaid diagram to a file."""
        generator = FlowchartGenerator()
        
        # Create a temporary directory for the test
        test_dir = "test_output"
        os.makedirs(test_dir, exist_ok=True)
        
        try:
            # Generate and save the diagram
            file_paths = generator.save_mermaid_diagram(IF_EXAMPLE, output_dir=test_dir)
            
            # Check that the file was created
            assert len(file_paths) == 1
            assert os.path.exists(file_paths[0])
            
            # Check the content of the file
            with open(file_paths[0], 'r') as f:
                content = f.read()
                assert "flowchart TD" in content
                assert "Function example" in content
        finally:
            # Clean up the test directory
            for file_path in os.listdir(test_dir):
                os.remove(os.path.join(test_dir, file_path))
            os.rmdir(test_dir)
            
    def test_terminal_nodes_connected_to_end(self):
        """Test that all terminal nodes (like returns) are connected to the End node."""
        generator = FlowchartGenerator()
        flowchart = generator.generate_mermaid_flowchart(IF_EXAMPLE)
        
        # The test needs to verify that terminal nodes are connected to End
        # but we need to check for the node IDs, not the labels
        assert " --> End" in flowchart  # Verify connections to End exist
        
        # Extract node IDs from the flowchart
        import re
        nodes = {}
        for line in flowchart.split('\n'):
            # Match lines like 'node4["Return: x"]'
            match = re.match(r'(node\d+)\["(Return: .+)"\]', line)
            if match:
                node_id, label = match.groups()
                nodes[label] = node_id
        
        # Check that return nodes are connected to End
        if "Return: x" in nodes:
            assert f"{nodes['Return: x']} --> End" in flowchart
        if "Return: -x" in nodes:
            assert f"{nodes['Return: -x']} --> End" in flowchart
        
        # Test with a more complex example that has multiple terminal nodes
        flowchart = generator.generate_mermaid_flowchart(BREAK_CONTINUE_EXAMPLE)
        
        # Extract node IDs again for the new flowchart
        nodes = {}
        for line in flowchart.split('\n'):
            match = re.match(r'(node\d+)\["(Return: .+)"\]', line)
            if match:
                node_id, label = match.groups()
                nodes[label] = node_id
        
        # Check that return nodes are connected to End
        if "Return: i" in nodes:
            assert f"{nodes['Return: i']} --> End" in flowchart
        if "Return: -1" in nodes:
            assert f"{nodes['Return: -1']} --> End" in flowchart
