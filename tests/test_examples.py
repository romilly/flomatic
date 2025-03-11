"""
Unit tests for the examples module.
"""

import os
import tempfile
import shutil
from unittest.mock import patch
from io import StringIO

import pytest
from flomatic.examples import (
    SOURCE_CODE, FOR_LOOP_CODE, BREAK_CONTINUE_CODE, WHILE_LOOP_CODE,
    IF_EXAMPLE, FOR_EXAMPLE, BREAK_CONTINUE_EXAMPLE, WHILE_EXAMPLE, CLASS_EXAMPLE,
    save_example_diagrams, print_example_diagrams
)


class TestExamples:
    """Test cases for the examples module."""
    
    def setup_method(self):
        """Set up a temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)
    
    def teardown_method(self):
        """Clean up after tests."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir)
    
    def test_example_code_snippets_are_valid_python(self):
        """Test that all example code snippets are valid Python."""
        # This will raise a SyntaxError if any code is invalid
        for code in [SOURCE_CODE, FOR_LOOP_CODE, BREAK_CONTINUE_CODE, WHILE_LOOP_CODE,
                     IF_EXAMPLE, FOR_EXAMPLE, BREAK_CONTINUE_EXAMPLE, WHILE_EXAMPLE, CLASS_EXAMPLE]:
            compile(code, '<string>', 'exec')
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_save_example_diagrams(self, mock_stdout):
        """Test that save_example_diagrams creates diagram files."""
        # Call the function
        save_example_diagrams()
        
        # Check that output directory was created
        assert os.path.exists("mermaid_diagrams")
        
        # Check that files were created
        files = os.listdir("mermaid_diagrams")
        assert len(files) > 0
        assert any(file.endswith(".mmd") for file in files)
        
        # Check that detailed directory was created
        assert os.path.exists("mermaid_diagrams/detailed")
        
        # Check that detailed files were created
        detailed_files = os.listdir("mermaid_diagrams/detailed")
        assert len(detailed_files) > 0
        assert any(file.endswith(".mmd") for file in detailed_files)
        
        # Check that output was printed
        output = mock_stdout.getvalue()
        assert "Saving diagrams to files..." in output
        assert "If statement diagram saved to:" in output
        assert "For loop diagram saved to:" in output
        assert "Break/continue diagram saved to:" in output
        assert "While loop diagram saved to:" in output
        assert "Class diagram saved to:" in output
        assert "Detailed class diagram saved to:" in output
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_example_diagrams(self, mock_stdout):
        """Test that print_example_diagrams outputs diagrams to console."""
        # Call the function
        print_example_diagrams()
        
        # Check that output was printed
        output = mock_stdout.getvalue()
        assert "Example with if statement:" in output
        assert "Example with for loop:" in output
        assert "Example with break and continue:" in output
        assert "Example with while loop:" in output
        assert "flowchart TD" in output
        assert "Start" in output
        assert "Function" in output
        assert "End" in output
