"""
Example demonstrating how to use PathResolver with XdmListNode for path handling.

This example shows the recommended way to integrate PathResolver into the existing
XDM codebase, particularly focusing on the path handling improvements for XdmListNode.
"""

from pathlib import Path
from typing import Optional
from tools.path import PathResolver
from tools.core.typedef import XdmListNode, YamlTreeHandler

def example_path_resolver_usage():
    # Initialize with a YAML root directory
    yaml_root = "u:/Users/Enlink/Documents/code/python/Xdm/DIO"
    path_resolver = PathResolver(yaml_root)
    
    print("Path Resolution Examples:")
    print("-" * 50)

    # Example 1: Converting user-provided paths to proper format
    user_paths = [
        "/vars/var1.yaml",  # Absolute path (relative to YAML root)
        "vars/var1.yaml",   # Relative path
        "./vars/var1.yaml", # Current directory relative path
        "../vars/var1.yaml" # Parent directory relative path
    ]
    
    print("\nExample 1: Resolving different path formats")
    print("User provided paths:")
    for path in user_paths:
        # Make all paths absolute relative to YAML root
        abs_path = path_resolver.make_absolute(path)
        # Get path relative to YAML root for storage/comparison
        rel_to_root = path_resolver.resolve_relative_to_root(abs_path)
        print(f"  Original: {path}")
        print(f"  Absolute: {abs_path}")
        print(f"  Relative to root: {rel_to_root}\n")

    # Example 2: Path comparison
    print("\nExample 2: Path comparison")
    path1 = r"vars\var1.yaml"
    path2 = "vars/var1.yaml"
    normalized1 = path_resolver.normalize_path(path1)
    normalized2 = path_resolver.normalize_path(path2)
    print(f"Path 1: {path1} -> {normalized1}")
    print(f"Path 2: {path2} -> {normalized2}")
    print(f"Paths are equal: {normalized1 == normalized2}")

    # Example 3: Working with base directories
    print("\nExample 3: Working with base directories")
    base_dir = f"{yaml_root}/ctr1"
    relative_path = "../vars/var1.yaml"
    resolved = path_resolver.resolve_relative_to_base(relative_path, base_dir)
    print(f"Base dir: {base_dir}")
    print(f"Relative path: {relative_path}")
    print(f"Resolved path: {resolved}")

    # Example 4: Recommended modification for XdmListNode
    print("\nExample 4: XdmListNode integration")
    print("See comments for recommended XdmListNode modifications")

    """
    Recommended modifications for XdmListNode:
    
    class XdmListNode:
        def __init__(self, template_name: str, usr_data: Optional[Dict[str, Any]], 
                     path_resolver: PathResolver, **kwargs):
            self.template_name = template_name
            self.usr_data = usr_data if usr_data is not None else {}
            self.path_resolver = path_resolver
            self.children = []
            self.children_text = kwargs.get("children_text", "")
            self.info = kwargs.get("info")  # System absolute path
            self.relative_path = None
            if self.info:
                # Store path relative to YAML root
                self.relative_path = self.path_resolver.resolve_relative_to_root(self.info)
            self.parent = None

        def find_by_yaml_path(self, yaml_path: str) -> Optional["XdmListNode"]:
            # Get root node
            root = self
            while root.parent:
                root = root.parent
                
            def find_node_with_path(node: "XdmListNode", target_path: str) -> Optional["XdmListNode"]:
                if not node.relative_path:
                    return None
                    
                # Compare normalized relative paths
                if self.path_resolver.normalize_path(node.relative_path) == \
                   self.path_resolver.normalize_path(target_path):
                    return node
                    
                for child in node.children:
                    result = find_node_with_path(child, target_path)
                    if result:
                        return result
                return None
            
            # Convert target path to relative format and search
            target_relative = self.path_resolver.resolve_relative_to_root(yaml_path)
            return find_node_with_path(root, target_relative)
    """

if __name__ == "__main__":
    example_path_resolver_usage()
