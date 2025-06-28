import xml.etree.ElementTree as ET
from typing import List, Tuple
import sys
import os

def find_nodes_under_xpath(xml_file: str, parent_xpath: str, node_types: List[str]) -> List[Tuple[str, dict]]:
    """
    Find specific node types under a given xpath.
    
    Args:
        xml_file: Path to XML file
        parent_xpath: XPath to parent node (e.g. ".//ctr")
        node_types: List of node types to find (e.g. ["a:a", "a:da"])
        
    Returns:
        List of tuples containing (node_tag, node_attributes)
    """
    try:
        # Verify file exists
        if not os.path.exists(xml_file):
            print(f"Error: File not found: {xml_file}", file=sys.stderr)
            return []

        # Parse XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        results = []
        
        # Convert absolute path to relative path
        search_path = parent_xpath.replace('//', './/').lstrip('/')
        search_path = search_path.replace('v:ctr', 'ctr')
        
        # Find all parent nodes matching the xpath
        parent_nodes = root.findall(parent_xpath)
        if not parent_nodes:
            print(f"No nodes found matching xpath: {parent_xpath}")
            return []
            
        for parent in parent_nodes:
            # For each parent, find direct children
            for child in parent:
                # Get the tag name without namespace
                tag = child.tag
                if '}' in tag:
                    tag = tag.split('}')[1]
                
                # Check if this child's tag matches any of our target types
                for node_type in node_types:
                    type_without_prefix = node_type.split(':')[1]
                    if tag == type_without_prefix:
                        # Store with original namespace prefix for output
                        original_tag = node_type
                        results.append((original_tag, child.attrib))
        
        return results
        
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}", file=sys.stderr)
        print(f"Make sure the XML file is well-formed and all namespaces are properly declared.", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        print(f"Current working directory: {os.getcwd()}", file=sys.stderr)
        print(f"File path being accessed: {os.path.abspath(xml_file)}", file=sys.stderr)
        return []

def main():
    # Get file path from command line argument or use default
    if len(sys.argv) > 1:
        xml_file = sys.argv[1]
    else:
        xml_file = rf"U:\Users\Enlink\Documents\参考文档\AUTOSAR_SampleProject_S32K144-master\plugins\Resource_TS_T40D2M10I1R0\config\Resource.xdm"
    
    print(f"Processing file: {xml_file}")
    
    nodes = find_nodes_under_xpath(
        xml_file, 
        ".//v:ctr",  # Find under any v:ctr node (using relative path)
        ["a:a", "a:da"]  # Look for a:a and a:da nodes
    )
    
    if nodes:
        print("\nFound nodes:")
        for tag, attrs in nodes:
            # Format attributes string
            attrs_str = " ".join([f'{k}="{v}"' for k, v in attrs.items()])
            print(f"<{tag} {attrs_str}/>")
    else:
        print("No matching nodes found.")

if __name__ == "__main__":
    main()
