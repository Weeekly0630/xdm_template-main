"""
yaml node处理
通过yaml中的特殊数据节点(CHILDREN)构建一个逻辑YAML树结构
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from .file_node import FileType, FileNode, DirectoryNode


class DataNode:
    def __init__(self, data: Optional[Dict[str, Any]], name: str):
        # See YamlNode as a DirectoryNode with additional YAML-specific data.
        self._node: DirectoryNode = DirectoryNode(name)
        self.data: Optional[Dict[str, Any]] = data

    def add_child(self, child: "DataNode") -> None:
        """Add a child DataNode to this node."""
        if child:
            self._node.add_node(child._node._node)
