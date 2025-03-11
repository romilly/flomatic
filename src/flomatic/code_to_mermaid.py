import ast
import os
import re

class FlowchartGenerator(ast.NodeVisitor):
    def __init__(self):
        self.flowchart = ["flowchart TD"]
        self.node_count = 0
        self.last_node = "Start"
        self.loop_start_node = None  # Reference to the current loop start for continue statements
        self.after_loop_node = None  # Reference to the node after the loop for break statements

    def add_node(self, label):
        self.node_count += 1
        node_name = f"node{self.node_count}"
        # Proper Mermaid syntax for nodes
        self.flowchart.append(f"{node_name}[\"{label}\"]")
        return node_name

    def add_connection(self, from_node, to_node):
        # Simple connection between nodes
        self.flowchart.append(f"{from_node} --> {to_node}")

    def generic_visit(self, node):
        # If in compact mode, only visit children without creating nodes for non-control flow elements
        if hasattr(self, 'compact') and self.compact:
            # Just continue visiting children
            super().generic_visit(node)
        else:
            # Provide a fallback for unhandled nodes that logs an info
            node_type = type(node).__name__
            new_node = self.add_node(f"{node_type}")
            self.add_connection(self.last_node, new_node)
            prev_node = self.last_node
            self.last_node = new_node
            super().generic_visit(node)
            # Restore the previous node as the last node
            self.last_node = prev_node

    def visit_FunctionDef(self, node):
        # Determine the full function name
        if hasattr(self, 'current_class') and self.current_class:
            full_func_name = f"{self.current_class}.{node.name}"
        else:
            full_func_name = node.name
            
        # Store function name if we need it later
        if hasattr(self, 'function_names'):
            self.function_names.append(full_func_name)
        
        # If we're targeting a specific function and this isn't it, skip processing its body
        if hasattr(self, 'target_function') and self.target_function and self.target_function != full_func_name:
            return
            
        # Always show function definitions, even in compact mode
        func_node = self.add_node(f"Function {node.name}")
        self.add_connection(self.last_node, func_node)
        self.last_node = func_node
        
        # Visit the body of the function
        for n in node.body:
            self.visit(n)

    def visit_If(self, node):
        # If condition
        cond_node = self.add_node(f"If: {ast.unparse(node.test)}")
        self.add_connection(self.last_node, cond_node)
        self.last_node = cond_node

        # Then branch
        then_node = self.add_node("Then")
        self.add_connection(cond_node, then_node)
        last_then = self.last_node
        self.last_node = then_node
        for n in node.body:
            self.visit(n)
        self.last_node = last_then

        # Else branch
        if node.orelse:
            else_node = self.add_node("Else")
            self.add_connection(cond_node, else_node)
            last_else = self.last_node
            self.last_node = else_node
            for n in node.orelse:
                self.visit(n)
            self.last_node = last_else

    def visit_For(self, node):
        # For loop header
        iter_str = f"For: {ast.unparse(node.target)} in {ast.unparse(node.iter)}"
        loop_start_node = self.add_node(iter_str)
        self.add_connection(self.last_node, loop_start_node)
        
        # Loop body
        loop_body_node = self.add_node("Loop Body")
        self.add_connection(loop_start_node, loop_body_node)
        
        # Save the current last node and create nodes for break and continue targets
        self.loop_start_node = loop_start_node  # For continue statements
        after_loop_node = self.add_node("After Loop")  # For break statements and normal loop exit
        self.after_loop_node = after_loop_node
        
        # Save the current last node
        last_before_body = self.last_node
        self.last_node = loop_body_node
        
        # Process the loop body
        for n in node.body:
            self.visit(n)
        
        # Connect back to the loop start for iteration (if not broken)
        self.add_connection(self.last_node, loop_start_node)
        
        # Connect loop start to after loop for when the loop ends
        self.add_connection(loop_start_node, after_loop_node)
        
        # Set the last node to after the loop
        self.last_node = after_loop_node
        
        # Handle else clause if it exists
        if node.orelse:
            else_node = self.add_node("Loop Else")
            self.add_connection(after_loop_node, else_node)
            last_else = self.last_node
            self.last_node = else_node
            for n in node.orelse:
                self.visit(n)
            self.last_node = last_else
        
        # Clean up loop context
        self.loop_start_node = None
        self.after_loop_node = None

    def visit_Return(self, node):
        # Handle return statements with and without values
        if node.value:
            return_node = self.add_node(f"Return: {ast.unparse(node.value)}")
        else:
            return_node = self.add_node("Return")
        self.add_connection(self.last_node, return_node)
        self.last_node = return_node
        
    def visit_While(self, node):
        # While loop condition
        cond_str = f"While: {ast.unparse(node.test)}"
        loop_start_node = self.add_node(cond_str)
        self.add_connection(self.last_node, loop_start_node)
        
        # Loop body
        loop_body_node = self.add_node("Loop Body")
        self.add_connection(loop_start_node, loop_body_node)
        
        # Save the current last node and create nodes for break and continue targets
        self.loop_start_node = loop_start_node  # For continue statements
        after_loop_node = self.add_node("After Loop")
        self.after_loop_node = after_loop_node
        
        # Process the loop body
        last_before_body = self.last_node
        self.last_node = loop_body_node
        for n in node.body:
            self.visit(n)
        
        # Connect back to the loop start for the next iteration check
        self.add_connection(self.last_node, loop_start_node)
        
        # Connect loop condition to after loop when condition is false
        self.add_connection(loop_start_node, after_loop_node)
        
        # Set the last node to after the loop
        self.last_node = after_loop_node
        
        # Handle else clause if it exists
        if node.orelse:
            else_node = self.add_node("Loop Else")
            self.add_connection(after_loop_node, else_node)
            last_else = self.last_node
            self.last_node = else_node
            for n in node.orelse:
                self.visit(n)
            self.last_node = last_else
        
        # Clean up loop context
        self.loop_start_node = None
        self.after_loop_node = None
        
    def visit_Break(self, node):
        if self.after_loop_node:
            break_node = self.add_node("Break")
            self.add_connection(self.last_node, break_node)
            self.add_connection(break_node, self.after_loop_node)
            # Create a new node to continue from after the break
            # This node won't actually be connected to in the normal flow
            # but we need to set last_node to something
            unreachable_node = self.add_node("Unreachable")
            self.last_node = unreachable_node
        else:
            # Handle break outside of loop context (shouldn't happen in valid Python)
            break_node = self.add_node("Break (Invalid)")
            self.add_connection(self.last_node, break_node)
            self.last_node = break_node
    
    def visit_Continue(self, node):
        if self.loop_start_node:
            continue_node = self.add_node("Continue")
            self.add_connection(self.last_node, continue_node)
            self.add_connection(continue_node, self.loop_start_node)
            # Create a new node to continue from after the continue
            # This node won't actually be connected to in the normal flow
            # but we need to set last_node to something
            unreachable_node = self.add_node("Unreachable")
            self.last_node = unreachable_node
        else:
            # Handle continue outside of loop context (shouldn't happen in valid Python)
            continue_node = self.add_node("Continue (Invalid)")
            self.add_connection(self.last_node, continue_node)
            self.last_node = continue_node

    def visit_ClassDef(self, node):
        # Store previous class context if any
        prev_class = getattr(self, 'current_class', None)
        # Set current class name
        self.current_class = node.name
        
        # If we're targeting a specific function that belongs to this class
        target_in_this_class = False
        if hasattr(self, 'target_function') and self.target_function:
            parts = self.target_function.split('.')
            if len(parts) > 1 and parts[0] == self.current_class:
                target_in_this_class = True
        
        # Only create a class node if we're not targeting a specific function
        # or if the target function is in this class
        if not hasattr(self, 'target_function') or not self.target_function or target_in_this_class:
            # Always show class definitions, even in compact mode
            class_node = self.add_node(f"Class {node.name}")
            self.add_connection(self.last_node, class_node)
            self.last_node = class_node
            
            # Visit all class body elements
            for n in node.body:
                self.visit(n)
        
        # Restore previous class context
        if prev_class:
            self.current_class = prev_class
        else:
            self.current_class = None
            
    def generate_mermaid_flowchart(self, source_code, target_function=None, compact=True):
        """Generate a Mermaid flowchart for the given source code.
        
        Args:
            source_code (str): The Python source code to generate a diagram for.
            target_function (str, optional): If provided, only generate a flowchart for this specific function.
                                           Can include class name as prefix (e.g., 'Calculator.multiply').
            compact (bool, optional): If True, only include control flow elements in the diagram.
                                    If False, include all AST nodes. Defaults to True.
            
        Returns:
            str: The generated Mermaid flowchart as a string.
        """
        self.flowchart = ["flowchart TD"]
        self.node_count = 0
        # Create a start node with proper syntax
        start_node = "Start"
        self.flowchart.append(f"{start_node}[\"Start\"]")
        self.last_node = start_node
        self.function_names = []
        self.current_class = None
        self.target_function = target_function
        self.compact = compact
        
        tree = ast.parse(source_code)
        
        # If we're targeting a specific function, find it in the AST and only process that
        if target_function:
            target_class = None
            target_method = target_function
            
            # Check if it's a class method
            if '.' in target_function:
                target_class, target_method = target_function.split('.')
            
            # Find the target function/method in the AST
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == target_class:
                    for child in node.body:
                        if isinstance(child, ast.FunctionDef) and child.name == target_method:
                            # Process just this method
                            if target_class:
                                self.current_class = target_class
                            self.visit_FunctionDef(child)
                            break
                    break
                elif isinstance(node, ast.FunctionDef) and node.name == target_method and not target_class:
                    # Process just this function
                    self.visit_FunctionDef(node)
                    break
        else:
            # Process the entire tree
            self.visit(tree)
        
        # Create an end node with proper syntax
        end_node = "End"
        self.flowchart.append(f"{end_node}[\"End\"]")
        return "\n".join(self.flowchart)
    
    def save_mermaid_diagram(self, source_code, output_dir=".", compact=True):
        """Generate Mermaid flowcharts for each function and save them to files named after the functions.
        
        Args:
            source_code (str): The Python source code to generate diagrams for.
            output_dir (str): Directory where to save the output files. Defaults to current directory.
            compact (bool, optional): If True, only include control flow elements in the diagram.
                                    If False, include all AST nodes. Defaults to True.
            
        Returns:
            list: List of file paths where diagrams were saved.
        """
        # First, get all function names by generating a complete flowchart
        temp_generator = FlowchartGenerator()
        temp_generator.generate_mermaid_flowchart(source_code, compact=compact)
        function_names = temp_generator.function_names.copy()
        
        if not function_names:
            # If no function names found, use a default name
            function_names = ["unnamed_function"]
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Save a separate diagram for each function
        saved_files = []
        for func_name in function_names:
            # Use a fresh generator for each function to avoid interference between diagrams
            function_generator = FlowchartGenerator()
            func_flowchart = function_generator.generate_mermaid_flowchart(source_code, target_function=func_name, compact=compact)
            
            # Create a safe filename
            safe_name = re.sub(r'[^\w\-_\.]', '_', func_name)
            file_path = os.path.join(output_dir, f"{safe_name}.mmd")
            
            # Write the flowchart to the file
            with open(file_path, 'w') as f:
                f.write(func_flowchart)
            
            saved_files.append(file_path)
        
        return saved_files
