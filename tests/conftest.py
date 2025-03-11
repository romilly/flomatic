"""
Pytest configuration file for Flomatic tests.
"""

import os
import pytest
import tempfile
import shutil


@pytest.fixture
def temp_test_dir():
    """Create a temporary directory for tests that is cleaned up afterward."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def example_code_snippets():
    """Return a dictionary of example code snippets for testing."""
    return {
        "if_example": """
def example(x):
    if x > 0:
        return x
    else:
        return -x
""",
        "for_example": """
def process_list(items):
    results = []
    for item in items:
        results.append(item * 2)
    return results
""",
        "while_example": """
def countdown(n):
    while n > 0:
        print(n)
        n -= 1
    print("Done!")
"""
    }
