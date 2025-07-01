"""
通用数据节点类，用于表示数据结构中的节点。
该类可以包含任意类型的数据，并且可以添加子节点。
它主要用于处理数据结构中的目录和文件节点。
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from .file_node import FileType, FileNode, DirectoryNode

class DataNode:
    def __init__(self, data: Dict[str, Any], name: str):
        # See YamlNode as a DirectoryNode with additional YAML-specific data.
        self._node: DirectoryNode = DirectoryNode(name)
        self.data: Dict[str, Any] = data

    # def add_child(self, child: "DataNode") -> None:
    #     """Add a child DataNode to this node."""
    #     if child:
    #         self._node.add_node(child._node._node)
