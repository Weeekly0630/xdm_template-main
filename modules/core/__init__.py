"""Core module for data driven generator"""

from enum import Enum
from typing import Protocol, Dict, Any, List, Optional, Iterator, runtime_checkable
from pathlib import Path
from ..node.data_node import DataNode


@runtime_checkable
class DataHandler(Protocol):
    """Protocol for data handlers

    所有的数据处理器必须实现以下方法:
    - create_data_tree: 从指定模式创建数据树
    - get_data_nodes: 根据文件路径模式查找数据节点
    - get_absolute_path: 获取节点的绝对路径
    """

    @property
    def preserved_template_key(self) -> str:
        """模板路径的键名

        Returns:
            str: 用于在数据中标识模板路径的键名
        """
        ...

    def create_data_tree(self, pattern: str) -> List[DataNode]:
        """从指定模式创建数据树

        Args:
            pattern: 文件路径模式，如 "root.yaml" 或 "**/root/*.yaml"

        Returns:
            List[Any]: 匹配模式的数据树列表

        Raises:
            错误处理由具体实现定义
        """
        ...

    def get_data_nodes(self, pattern: str) -> List[DataNode]:
        """根据文件路径模式查找数据节点

        Args:
            pattern: 文件路径模式，如 "*.yaml" 或 "**/config/*.yaml"

        Returns:
            List[Any]: 匹配的数据节点列表
        """
        ...

    def get_absolute_path(self, node: Any) -> str:
        """获取节点的绝对路径

        Args:
            node: 数据节点

        Returns:
            str: 节点的绝对路径
        """
        ...


@runtime_checkable
class TemplateHandler(Protocol):
    """Protocol for template handlers"""

    @property
    def config(self) -> Any:
        """Get handler configuration
        
        Returns:
            Any: Handler configuration containing preserved_children_key
        """
        ...

    def render_template(self, template_path: str, data: Dict[str, Any]) -> str:
        """Render a template with data

        Args:
            template_path: Path to the template file
            data: Data to render the template with

        Returns:
            str: The rendered template
        """
        ...


class GeneratorErrorType(Enum):
    """Error types for generator"""

    DATA_INIT_ERROR = "data_init_error"
    TEMPLATE_INIT_ERROR = "template_init_error"
    RENDER_ERROR = "render_error"
    TEMPLATE_NOT_FOUND = "template_not_found"


class GeneratorError(Exception):
    """Base class for generator errors"""

    def __init__(self, error_type: GeneratorErrorType, message: str) -> None:
        self.error_type = error_type
        self.message = message
        super().__init__(f"{error_type.value}: {message}")


def validate_data_handler(handler: Any) -> None:
    """验证数据处理器是否实现了所有必要的方法

    Args:
        handler: 要验证的处理器实例

    Raises:
        GeneratorError: 如果处理器没有实现所有必要的方法
    """
    if not isinstance(handler, DataHandler):
        raise GeneratorError(
            GeneratorErrorType.DATA_INIT_ERROR,
            "Data handler must implement DataHandler protocol",
        )


def validate_template_handler(handler: Any) -> None:
    """验证模板处理器是否实现了所有必要的方法"""
    if not isinstance(handler, TemplateHandler):
        raise GeneratorError(
            GeneratorErrorType.TEMPLATE_INIT_ERROR,
            "Template handler must implement TemplateHandler protocol",
        )


def validate_data_context(data: Dict[str, Any], template_key: str) -> None:
    """验证数据上下文是否包含必要的键"""
    if template_key not in data:
        raise GeneratorError(
            GeneratorErrorType.TEMPLATE_NOT_FOUND,
            f"Missing required key '{template_key}' in data",
        )


def validate_render_result(result: Optional[str], template_path: str) -> None:
    """验证渲染结果是否有效"""
    if result is None:
        raise GeneratorError(
            GeneratorErrorType.RENDER_ERROR,
            f"Failed to render template: {template_path}",
        )
