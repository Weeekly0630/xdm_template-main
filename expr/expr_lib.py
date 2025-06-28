from typing import Dict, Any, Union
from pathlib import Path
from .expr_loader import XdmElementLoader
from .xdm_expr_typedef import XdmElement

class ExpressionLibrary:
    """XDM Expression Library - provides interface for processing XDM expressions."""
    
    def __init__(self):
        """Initialize the expression library."""
        self._loader = XdmElementLoader()
        
    def set_root_node(self, root_node):
        """设置根节点"""
        self._loader.set_root_node(root_node)

    def set_current_node(self, node):
        """设置当前处理的节点上下文。"""
        self._loader.set_current_node(node)
        
    def process_expression(self, expr_data: Union[Dict[str, Any], str]) -> XdmElement:
        """Process a single expression definition.
        
        Args:
            expr_data: Expression definition, either as:
                      - A dictionary containing expression definition
                      - A string for simple expressions
                      
        Returns:
            XdmElement: The processed expression result
        """
        return self._loader._build_value(expr_data)
        
    def load_expressions(self, yaml_path: Union[str, Path]) -> Dict[str, XdmElement]:
        """Load all expressions from a YAML file.
        
        Args:
            yaml_path: Path to the YAML file containing expressions
            
        Returns:
            Dict[str, XdmElement]: Dictionary of processed expressions
        """
        return self._loader.load_from_yaml(yaml_path)
        
    def load_expression(self, yaml_path: Union[str, Path], expr_name: str) -> XdmElement:
        """Load a specific expression from a YAML file.
        
        Args:
            yaml_path: Path to the YAML file containing expressions
            expr_name: Name of the expression to load
            
        Returns:
            XdmElement: The processed expression
        """
        return self._loader.load_from_yaml(yaml_path, expr_name)

def get_expression_library() -> ExpressionLibrary:
    """Factory function to get an ExpressionLibrary instance.
    
    Returns:
        ExpressionLibrary: A new ExpressionLibrary instance
    """
    return ExpressionLibrary()
