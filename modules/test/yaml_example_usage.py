import os
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add the parent directory to sys.path to import modules
current_dir = Path(__file__).parent
sys.path.append(str(current_dir.parent.parent))

from modules.node.data_node import DataNode
from modules.yaml.yaml_handler import YamlDataTreeHandler

def demonstrate_yaml_handler():
    """展示YamlDataTreeHandler的用法"""
    config = {
        "root_path": str(current_dir / "yaml_example"),
        "file_pattern": ["*.yaml"],
    }
    
    try:
        # 创建YAML处理器实例
        handler = YamlDataTreeHandler(config)
        
        # 1. 显示文件树结构
        print("\n=== File Tree Structure ===")
        print(handler.file_tree.serialize_tree())
        
        # 2. 创建数据树（从根节点开始）
        print("\n=== Creating Data Tree ===")
        data_trees = handler.create_data_tree("root.yaml")
        for tree in data_trees:
            print(f"\nData Tree (root: {tree.name}):")
            print(tree.serialize_tree(indent=2))
            
        # 3. 使用不同的路径模式查找数据节点
        patterns = [
            "*.yaml",              # 根目录下的YAML文件
            "**/children/*.yaml",  # children目录下的YAML文件
            "**/*.yaml"           # 所有YAML文件
        ]
        
        for pattern in patterns:
            print(f"\n=== Finding Data Nodes ({pattern}) ===")
            nodes = handler.get_data_nodes(pattern)
            print(f"Found {len(nodes)} nodes:")
            for node in nodes:
                print(f"- {node.name}: {node.data}")
                
        # 4. 深度优先遍历数据节点
        if data_trees:
            root = data_trees[0]
            print("\n=== Depth-First Data Traversal ===")
            print("Traversing from root node:")
            for node in root.get_data():
                print(f"- {node}")
                
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    print("=== YamlDataTreeHandler Usage Example ===")
    demonstrate_yaml_handler()

if __name__ == "__main__":
    main()
