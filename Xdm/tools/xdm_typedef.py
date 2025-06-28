from dataclasses import dataclass, field
from typing import Optional, Union, List, Dict, Any
from enum import Enum
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from pathlib import Path
import glob
import yaml


@dataclass
class XdmListNode: ...


class JinjaEnvironment:
    """A simple class to handle Jinja2 environment setup."""

    def __init__(self, template_dir: str):
        """Initialize the Jinja2 environment with the specified template directory."""
        self.template_dir = template_dir
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            undefined=StrictUndefined,  # 使用StrictUndefined确保未定义变量会抛出异常
        )

    def render_node(self, node: XdmListNode) -> str:
        """递归渲染节点及其子节点"""
        try:
            # 1. 先递归渲染所有子节点
            children_texts = []
            for child in node.children:
                if not isinstance(child, XdmListNode):
                    raise TypeError(f"Child {child} is not an instance of XdmListNode")
                child_text = self.render_node(child)
                children_texts.append(child_text)

            # 2. 合并子节点渲染结果
            node.children_text = "\n".join(children_texts)

            # 3. 获取并验证模板
            if not node.template_name:
                raise ValueError("Template name is required")
            template = self.env.get_template(node.template_name)

            # 4. 渲染当前节点，加强错误处理
            try:
                context = template.render(
                    children_text=node.children_text, **(node.usr_data or {})
                )
                return context
            except Exception as e:
                raise ValueError(
                    f"Failed to render template {node.template_name}: {str(e)}"
                )

        except Exception as e:
            # 5. 统一的错误处理
            error_info = [
                "Error rendering node:",
                node.get_debug_info(),
                f"Error: {str(e)}",
            ]
            raise RuntimeError("\n".join(error_info))


@dataclass
class XdmListNode:
    template_name: str
    usr_data: Optional[Dict[str, Any]]
    children: List["XdmListNode"]
    children_text: Optional[str] = ""
    info: Optional[str] = None  # Additional field to store file path or other info

    def __str__(self) -> str:
        return f"XdmListNode(template='{self.template_name}', data={self.usr_data}) : {self.info}"

    def add_child(self, child: "XdmListNode"):
        """Add a child node to this list node."""
        self.children.append(child)

    def get_debug_info(self, indent: int = 0) -> str:
        """获取节点的详细调试信息，包括子节点"""
        info = []
        prefix = "  " * indent
        info.append(f"{prefix}Template: {self.template_name}")
        info.append(f"{prefix}Data: {self.usr_data}")
        info.append(f"{prefix}Info: {self.info}")
        # if self.children:
        #     info.append(f"{prefix}Children:")
        #     for child in self.children:
        #         info.append(child.get_debug_info(indent + 1))
        return "\n".join(info)


class YamlTreeHandler:
    def __init__(self, yaml_root_path: str):
        """Initialize the handler with the root path for YAML files."""
        # check path exists
        if not Path(yaml_root_path).exists():
            raise FileNotFoundError(
                f"The specified YAML root path does not exist: {yaml_root_path}"
            )
        self.yaml_root_path = Path(yaml_root_path)

    @staticmethod
    def load_yaml_file(yaml_path: str) -> dict:
        """Load a YAML file and return its contents as a dictionary."""
        try:
            with open(yaml_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data if data is not None else {}
        except Exception as e:
            print(f"Error loading YAML file {yaml_path}: {e}")
            return {}

    @staticmethod
    def get_template_name(yaml_data: dict) -> str:
        """Get the template name from YAML data."""
        template_type = yaml_data.get("TEMPLATE_NAME", "")
        if template_type == "":
            raise ValueError("TEMPLATE_NAME is required in the YAML data")
        return f"{template_type}.xdm"

    @staticmethod
    def resolve_child_paths(root_path: str, child_pattern: str) -> List[str]:
        """Resolve glob patterns to actual file paths.

        Args:
            root_path: The base path to resolve relative patterns from
            child_pattern: Pattern that can be:
                - Direct file path: "./chc/a.yaml", "./chc/temp/b.yaml"
                - Glob pattern: "./data/*", "chc/**/*.yaml"

        Examples:
            CHILDREN in yaml:
            CHILDREN:
            - "./chc/a.yaml"           # 具体文件
            - "./data/*"               # 目录下所有文件
            - "../sibling/*.yaml"      # 父目录下所有yaml文件
            - "test/**/*.yaml"         # 递归查找所有yaml文件

        Returns:
            List of matched file paths
        """
        root = Path(root_path)

        # 标准化路径分隔符
        child_pattern = child_pattern.replace("\\", "/")

        # 处理 ./ 开头的相对路径
        if child_pattern.startswith("./"):
            child_pattern = child_pattern[2:]

        # 处理 ../ 开头的父目录引用
        parent_count = 0
        while child_pattern.startswith("../"):
            parent_count += 1
            child_pattern = child_pattern[3:]

        # 计算实际的根路径
        actual_root = root
        for _ in range(parent_count):
            actual_root = actual_root.parent

        # 组合完整的查找模式
        full_pattern = str(actual_root / child_pattern)

        # 使用glob查找匹配的文件
        matched_files = glob.glob(full_pattern, recursive=True)
        print(full_pattern, matched_files)
        # 只返回文件（排除目录）
        return [path for path in matched_files if Path(path).is_file()]

    @staticmethod
    def process_yaml(yaml_abs_path: str) -> XdmListNode:
        """Process a single YAML file and its children."""
        # Load YAML content
        yaml_data = YamlTreeHandler.load_yaml_file(yaml_abs_path)

        # Create node for current YAML
        current_node = XdmListNode(
            template_name=YamlTreeHandler.get_template_name(yaml_data),
            usr_data=yaml_data,
            children_text="",
            children=[],
            info=yaml_abs_path,
        )

        # Process children if defined
        if "CHILDREN" in yaml_data:
            yaml_dir = Path(yaml_abs_path).parent
            for child_pattern in yaml_data["CHILDREN"]:
                if not isinstance(child_pattern, str):
                    raise ValueError(
                        f"CHILDREN must be a list of strings, got {type(child_pattern)}"
                    )
                elif not child_pattern:
                    continue
                child_paths = YamlTreeHandler.resolve_child_paths(
                    yaml_dir, child_pattern
                )
                for child_path in child_paths:
                    child_node = YamlTreeHandler.process_yaml(child_path)
                    current_node.add_child(child_node)

        return current_node

    def generate(self) -> List[XdmListNode]:
        """Generate a list of XdmListNode from the YAML files."""
        result_nodes: List[XdmListNode] = []
        pattern = str(self.yaml_root_path / "*.yaml")
        print(pattern)
        for yaml_abs_path in glob.glob(pattern):
            root_node = YamlTreeHandler.process_yaml(yaml_abs_path)
            result_nodes.append(root_node)

        return result_nodes
