import yaml
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from pathlib import Path

from ..node.data_node import DataNode


@dataclass
class YamlConfig:
    root_path: Path
    encoding: str = "utf-8"
    # schema: Optional[Dict] = None

    @classmethod
    def validate(cls, config: Dict[str, Any]) -> "YamlConfig":
        """验证配置并返回配置对象"""
        if "root_path" not in config:
            raise ValueError("Missing required field 'root_path'")

        root_path = Path(config["root_path"])
        if not root_path.exists():
            raise ValueError(f"root_path {root_path} does not exist")

        return cls(
            root_path=root_path,
            encoding=config.get("encoding", "utf-8"),
            # schema=config.get("schema"),
        )


class YamlDataTreeHandler:
    """Yaml data tree"""

    def __init__(self, config: Dict[str, Any]) -> None:
        # Load .yaml file from root_path and build a tree structure
        self.config = YamlConfig.validate(config)
        self.data_tree: DataNode = DataNode(data=None, name=self.config.root_path.name)

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

    def get_data(self) -> Optional[dict]:
        """ """
        pass
