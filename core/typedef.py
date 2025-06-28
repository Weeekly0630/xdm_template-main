from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from pathlib import Path
import glob
import yaml

@dataclass
class XdmListNode:
    template_name: str
    usr_data: Optional[Dict[str, Any]]
    children: List["XdmListNode"]
    children_text: Optional[str] = ""
    info: Optional[str] = None  # Additional field to store file path or other info
    parent: Optional["XdmListNode"] = None  # Reference to parent node

    def __str__(self) -> str:
        return f"XdmListNode(template='{self.template_name}', data={self.usr_data}) : {self.info}"

    def add_child(self, child: "XdmListNode"):
        """Add a child node to this list node."""
        child.parent = self  # Set parent reference
        self.children.append(child)

    def get_debug_info(self, indent: int = 0) -> str:
        """获取节点的详细调试信息，包括子节点"""
        info = []
        prefix = "  " * indent
        info.append(f"{prefix}Template: {self.template_name}")
        info.append(f"{prefix}Data: {self.usr_data}")
        info.append(f"{prefix}Info: {self.info}")
        return "\n".join(info)

    def find_child_by_name(self, name: str) -> Optional["XdmListNode"]:
        """Find a direct child node by its name."""
        if not self.children:
            return None
            
        for child in self.children:
            if child.usr_data and child.usr_data.get("name") == name:
                return child
        return None

    def find_descendant_by_name(self, name: str) -> Optional["XdmListNode"]:
        """Find a descendant node by its name (searches entire subtree)."""
        # First check direct children
        child = self.find_child_by_name(name)
        if child:
            return child
            
        # Then recursively check children's descendants
        for child in self.children:
            descendant = child.find_descendant_by_name(name)
            if descendant:
                return descendant
        return None

    def get_relative_xpath_to(self, target: "XdmListNode") -> str:
        """Calculate relative XPath expression from this node to target node."""
        from ..node import get_relative_xpath
        return get_relative_xpath(self, target)

    def find_by_absolute_path(self, path: str) -> Optional["XdmListNode"]:
        """Find a node using absolute path from root."""
        if not path.startswith('/'):
            raise ValueError("Path must be absolute (start with '/')")
            
        # Get root node
        current = self
        while current.parent:
            current = current.parent
            
        # Remove leading slash and split path
        parts = path.strip('/').split('/')
        
        for part in parts:
            current = current.find_child_by_name(part)
            if not current:
                return None
                
        return current

    def find_by_yaml_path(self, yaml_path: str) -> Optional["XdmListNode"]:
        """根据YAML文件路径查找节点"""
        # 获取根节点
        root = self
        while root.parent:
            root = root.parent
            
        def find_node_with_path(node: "XdmListNode", target_path: str) -> Optional["XdmListNode"]:
            # 检查当前节点
            if node.info == target_path:
                return node
                
            # 递归检查子节点
            for child in node.children:
                result = find_node_with_path(child, target_path)
                if result:
                    return result
            return None
            
        return find_node_with_path(root, str(Path(yaml_path).resolve()))

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
    def calculate_relative_path(from_path: str, to_path: str) -> str:
        """Calculate the relative path from one path to another."""
        from_path = Path(from_path).resolve()
        to_path = Path(to_path).resolve()
        return str(to_path.relative_to(from_path))
    
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
        return f"{template_type}"

    @staticmethod
    def resolve_child_paths(root_path: str, child_pattern: str) -> List[str]:
        """Resolve glob patterns to actual file paths."""
        root = Path(root_path)
        child_pattern = child_pattern.replace("\\", "/")

        if child_pattern.startswith("./"):
            child_pattern = child_pattern[2:]

        parent_count = 0
        while child_pattern.startswith("../"):
            parent_count += 1
            child_pattern = child_pattern[3:]

        actual_root = root
        for _ in range(parent_count):
            actual_root = actual_root.parent

        full_pattern = str(actual_root / child_pattern)
        matched_files = glob.glob(full_pattern, recursive=True)
        print(full_pattern, matched_files)
        return [path for path in matched_files if Path(path).is_file()]

    @staticmethod
    def process_expressions_in_data(data: Any, expr_lib) -> Any:
        """Recursively process expressions in the data structure."""
        if isinstance(data, dict):
            if "expr" in data:
                result = {k: v for k, v in data.items()}
                result["expr"] = str(expr_lib.process_expression(data["expr"]))
                return result
            return {k: YamlTreeHandler.process_expressions_in_data(v, expr_lib) 
                   for k, v in data.items()}
        
        if isinstance(data, list):
            return [YamlTreeHandler.process_expressions_in_data(item, expr_lib) 
                   for item in data]
        
        return data

    @staticmethod
    def process_yaml(yaml_abs_path: str) -> XdmListNode:
        """Process a single YAML file and its children."""
        yaml_data = YamlTreeHandler.load_yaml_file(yaml_abs_path)
        
        # TODO: 取消在处理yaml时对表达式的处理，改为在渲染时处理
        # from ..expr.expr_lib import get_expression_library
        # expr_lib = get_expression_library()
        # processed_data = YamlTreeHandler.process_expressions_in_data(yaml_data, expr_lib)

        current_node = XdmListNode(
            template_name=YamlTreeHandler.get_template_name(yaml_data),
            usr_data=yaml_data,
            children_text="",
            children=[],
            info=yaml_abs_path,
        )

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

    def generate(self) -> XdmListNode:
        """
        生成以root_path为根的树结构。
        从根目录的YAML文件开始构建。
        """
        # 创建虚拟根节点
        root_node = XdmListNode(
            template_name="",  # 虚拟根节点不需要模板
            usr_data={"name": self.yaml_root_path.name},  # 使用目录名作为节点名
            children=[],
            info=str(self.yaml_root_path)
        )

        # 只处理根目录下的YAML文件
        for yaml_path in self.yaml_root_path.glob("*.yaml"):
            # 处理每个YAML文件及其子节点
            node = self.process_yaml(str(yaml_path))
            root_node.add_child(node)

        return root_node
