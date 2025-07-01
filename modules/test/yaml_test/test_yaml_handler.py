import os
import sys
import unittest
from pathlib import Path

# Add the parent directory to sys.path to import modules
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from modules.yaml.yaml_handler import YamlDataTreeHandler

class TestYamlHandler(unittest.TestCase):
    """Test cases for YamlDataTreeHandler"""

    def setUp(self):
        """Set up test configuration"""
        self.base_config = {
            "root_path": str(Path(__file__).parent / "configs"),
            "file_pattern": ["*.yaml"],
        }

    def test_basic_yaml_tree(self):
        """Test basic YAML tree functionality with valid files"""
        handler = YamlDataTreeHandler(self.base_config)
        # print(handler.file_tree.serialize_tree())
        # Test file tree structure
        self.assertGreater(len(handler.file_tree.children), 0, "File tree should have children")
        
        # Test data tree list
        self.assertGreater(len(handler.data_tree_list), 0, "Data tree list should not be empty")
        
        # Find and verify root node
        root_node = next(
            (node for node in handler.data_tree_list if node._node.name == "root.yaml"),
            None
        )
        self.assertIsNotNone(root_node, "Root node should exist")
        if root_node:  # Type guard for root_node
            self.assertEqual(root_node.data["TEMPLATE_PATH"], "templates/root.tmpl")
            self.assertIsInstance(root_node.data["CHILDREN_PATH"], list)
            self.assertEqual(len(root_node.data["CHILDREN_PATH"]), 2)

            # Verify root has both child1 and child2 as direct children
            child_names = [child.name for child in root_node._node.children]
            self.assertIn("child1.yaml", child_names, "Root should have child1 as direct child")
            self.assertIn("child2.yaml", child_names, "Root should have child2 as direct child")

        # Find child1 node and verify it has no children
        child1_data = next(
            (node for node in handler.data_tree_list if node._node.name == "child1.yaml"),
            None
        )
        self.assertIsNotNone(child1_data, "Child1 data should exist")
        if child1_data:  # Type guard for child1_data
            self.assertEqual(child1_data.data["data"]["type"], "sub1")
            self.assertEqual(len(child1_data._node.children), 0, "Child1 should have no children")


if __name__ == '__main__':
    unittest.main()
