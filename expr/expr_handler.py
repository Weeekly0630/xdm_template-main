from typing import Optional, List, Dict
import sys
import os

# Ensure the tools directory is in sys.path for relative import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from xdm_expr_typedef import (
    XdmExpression,
    XdmXPathValue,
    XdmFunctionValue,
    XdmOperator,
    XdmFunctionLibrary,
    XdmFunctionType,
)

def create_test_expression() -> XdmExpression:
    """Creates a test expression to demonstrate XDM expression functionality."""
    # Initialize function library
    func_lib = XdmFunctionLibrary()

    # Create a complex expression with nested XPath and function calls
    expr = XdmExpression(
        left_value=XdmXPathValue(
            value=[
                "../path/to/",
                "some/node/",
                XdmFunctionValue(
                    value=["\"ggg\""],
                    func_type=XdmFunctionType.GET_CHILDREN,
                    func_lib=func_lib,
                ),
            ]
        ),
        right_value=XdmFunctionValue(
            value=[XdmXPathValue(value=["other/path/to/node"])],
            func_type=XdmFunctionType.GET_CHILDREN,
            func_lib=func_lib,
        ),
        operator=XdmOperator.EQUAL,
    )
    return expr

def main():
    # Create and print a test expression
    expr = create_test_expression()
    print("Test Expression:")
    print(str(expr))

if __name__ == "__main__":
    main()
