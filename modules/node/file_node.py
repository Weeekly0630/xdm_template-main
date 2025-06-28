"""
FileNode 模块
提供文件和目录节点的表示和操作。
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from .node import ListNode


class FileType(Enum):
    FILE = "file"
    DIRECTORY = "directory"


class FilePathResolver:
    @staticmethod
    def normalize_path(path: str) -> str:
        """Normalize the file path to a standard format."""
        # Replace backslashes with forward slashes for consistency
        path = path.replace("\\", "/").strip("/")
        # Remove any leading or trailing slashes
        path = path.replace("//", "/")  # Remove any double slashes
        # Lowercase the path for case-insensitive comparison
        path = path.lower()
        return path


class __FileNode:
    """Generic file list node class for representing files and directories in a tree structure."""

    def __init__(self, node_name: str, node_type: FileType):
        self.parent: Optional["__FileNode"] = None  # parent node, None for root node

        # d-list for parent's children
        self._parent_list = ListNode()

        # file name and type
        self.name = node_name
        self.type = node_type

    def set_parent(self, parent: Optional["__FileNode"]) -> None:
        """设置父节点"""
        self.parent = parent

    @staticmethod
    def _get_ancestors(node: "__FileNode") -> List["__FileNode"]:
        """获取节点的所有祖先节点（包括自身）"""
        ancestors: List[__FileNode] = []
        current: Optional["__FileNode"] = node
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors

    @staticmethod
    def get_relative_path(from_node: "__FileNode", to_node: "__FileNode") -> str:
        """计算从一个节点到另一个节点的相对路径"""
        relative_path = ""
        # 获取两个节点的祖先列表
        from_ancestors = __FileNode._get_ancestors(from_node)
        to_ancestors = __FileNode._get_ancestors(to_node)
        # 找到最近的公共祖先
        common_ancestor = None
        for ancestor in from_ancestors:
            if ancestor in to_ancestors:
                common_ancestor = ancestor
                break
        if not common_ancestor:
            relative_path = ""
        else:
            # 计算从from_node到common_ancestor的上级路径
            from_distance = from_ancestors.index(common_ancestor)
            to_distance = to_ancestors.index(common_ancestor)
            # 向上移动到公共祖先
            relative_path += "../" * from_distance
            # 向下移动到目标节点
            relative_path += "/".join(
                ancestor.name for ancestor in to_ancestors[to_distance + 1 :]
            )

        return relative_path

    @staticmethod
    def get_absolute_path(node: "__FileNode") -> str:
        """获取节点的绝对路径"""
        ancestors = __FileNode._get_ancestors(node)
        # 反转祖先列表并提取名称
        path_parts = [
            ancestor.name for ancestor in reversed(ancestors) if ancestor.name
        ]
        # 使用斜杠连接路径部分
        absolute_path = "/".join(path_parts)
        return absolute_path if absolute_path else "/"


class DirectoryNode:
    """List Node for Type directory"""

    def __init__(self, dir_name: str):
        self._node: __FileNode = __FileNode(dir_name, FileType.DIRECTORY)
        self.children_list: ListNode = ListNode()

    def add_node(self, node: __FileNode) -> None:
        """将节点添加到当前目录的子节点列表中"""
        if not isinstance(node, __FileNode):
            raise TypeError("Expected a __FileNode instance.")
        # add the node to the directory's children list
        self.children_list.insert_after(node._parent_list)
        node.set_parent(self._node)

    def create_file(self, file_name: str) -> "FileNode":
        """在当前目录下创建一个文件"""
        file_node: FileNode = FileNode(file_name)
        self.add_node(file_node._node)
        return file_node

    def create_directory(self, dir_name: str) -> "DirectoryNode":
        """在当前目录下创建一个子目录"""
        dir_node: DirectoryNode = DirectoryNode(dir_name)
        self.add_node(dir_node._node)
        return dir_node


class FileNode:
    """List Node for Type file"""

    def __init__(self, file_name: str):
        self._node = __FileNode(file_name, FileType.FILE)

    def isBinded(self) -> bool:
        """检查文件是否已绑定到目录"""
        return self._node.parent is not None

    def unbind(self) -> None:
        """解除文件与目录的绑定"""
        if self._node.parent:
            # 从父目录的子节点列表中移除当前文件节点
            self._node._parent_list.remove()
            # 清除父节点引用
            self._node.set_parent(None)

    def bind(self, directory: DirectoryNode) -> None:
        """将文件绑定到指定目录"""
        if not isinstance(directory, DirectoryNode):
            raise TypeError("Expected a DirectoryNode instance.")

        # 检查文件是否已经绑定到其他目录
        if self.isBinded():
            raise ValueError(
                f"File {self._node.name} is already bound to a directory. Unbind it first."
            )

        # 设置当前文件的父节点为目标目录
        self._node.set_parent(directory._node)

        # 将当前文件节点插入到目标目录的子节点列表中
        directory.add_node(self._node)

    def move_to_directory(self, directory: DirectoryNode) -> None:
        """将文件移动到指定目录"""
        if not isinstance(directory, DirectoryNode):
            raise TypeError("Expected a DirectoryNode instance.")
        # unbind the file from its current parent if it exists
        self.unbind()

        # bind the file to the new directory
        self.bind(directory)
