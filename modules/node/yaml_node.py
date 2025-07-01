# """
# yaml node处理
# 通过yaml中的特殊数据节点(CHILDREN)构建一个逻辑YAML树结构
# """

# from enum import Enum
# from typing import Optional, List, Dict
# from dataclasses import dataclass

# from .file_node import FileType, FileNode, DirectoryNode


# class YamlNode(DirectoryNode):
#     def __init__(self, yaml_name: str, data: dict, parent: Optional["YamlNode"]):
#         super().__init__(yaml_name, parent)
#         self.data: dict = data