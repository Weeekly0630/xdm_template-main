import xml.etree.ElementTree as ET
from typing import List, Tuple
import sys
import os

def find_nodes_under_xpath(xml_file: str, parent_xpath: str, node_types: List[str]) -> List[Tuple[str, dict]]:
    """
    Find specific node types under a given xpath, ignoring namespaces.
    
    Args:
        xml_file: Path to XML file
        parent_xpath: XPath to parent node (e.g. "ctr" to find all ctr nodes)
        node_types: List of node types to find without namespaces (e.g. ["a", "da"])
        
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
        
        # Use ElementTree's namespace handling to find nodes by local name
        # First get all elements recursively
        all_elements = root.findall(".//*")
        # Then filter by local name
        parent_nodes = [
            elem for elem in all_elements 
            if elem.tag.split('}')[-1] == parent_xpath.split(':')[-1]
        ]
        
        if not parent_nodes:
            print(f"No nodes found matching: {parent_xpath}")
            return []
            
        for parent in parent_nodes:
            # For each parent, find direct children
            for child in parent:
                # Get the local tag name without namespace
                tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                
                # Check if this child's tag matches any of our target types
                for node_type in node_types:
                    # Remove any namespace prefix from search type
                    search_type = node_type.split(':')[-1]
                    if tag == search_type:
                        # Store result with original tag
                        results.append((tag, child.attrib))
        
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
        xml_file = rf"U:\Users\Enlink\Documents\参考文档\AUTOSAR_SampleProject_S32K144-master\plugins\Can_TS_T40D2M10I1R0\config\Can.xdm"
    
    print(f"Processing file: {xml_file}")
    
    nodes = find_nodes_under_xpath(
        xml_file, 
        "ctr",  # Find under any ctr node (namespace agnostic)
        ["a", "da"]  # Look for a and da nodes (without namespace prefixes)
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
