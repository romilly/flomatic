"""
Test that the flomatic module can be imported correctly.
"""

def test_import_flomatic():
    """Test that the flomatic module can be imported."""
    try:
        import flomatic
        assert True
    except ImportError:
        assert False, "Failed to import flomatic module"

def test_import_code_to_mermaid():
    """Test that the code_to_mermaid module can be imported."""
    try:
        from flomatic import code_to_mermaid
        assert True
    except ImportError:
        assert False, "Failed to import code_to_mermaid module"

def test_import_flowchart_generator():
    """Test that the FlowchartGenerator class can be imported."""
    try:
        from flomatic.code_to_mermaid import FlowchartGenerator
        assert True
    except ImportError:
        assert False, "Failed to import FlowchartGenerator class"

def test_import_examples():
    """Test that the examples module can be imported."""
    try:
        from flomatic import examples
        assert True
    except ImportError:
        assert False, "Failed to import examples module"
