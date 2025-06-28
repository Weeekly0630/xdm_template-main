"""XDM Expression Package

This package provides functionality for processing XDM expressions.

The main interface is provided through expr_lib.py, which can be used to:
- Process individual expressions
- Load expressions from YAML files
- Get expression results as strings

Example usage:
    from expr.expr_lib import get_expression_library
    
    expr_lib = get_expression_library()
    result = expr_lib.process_expression(expr_data)
"""

from .expr_lib import get_expression_library

__all__ = ['get_expression_library']
