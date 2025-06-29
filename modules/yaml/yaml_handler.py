import yaml
from typing import Optional, List, Dict, Any, Iterator
from dataclasses import dataclass
from pathlib import Path

from ..node.data_node import DataNode


@dataclass
class YamlConfig:
    """YAML configuration with preserved keys for template and children paths"""

    root_path: Path
    encoding: str = "utf-8"
    # These keys are moved from DataDrivenGeneratorConfig since they are specific to YAML data handling
    preserved_template_key: str = "TEMPLATE_PATH"
    preserved_children_key: str = "CHILDREN_PATH"

    @classmethod
    def validate(cls, config: Dict[str, Any]) -> "YamlConfig":
        """Validate configuration and return config object

        Args:
            config: Dictionary containing configuration values.
                Required:
                    - root_path: Path to the root YAML file
                Optional:
                    - encoding: File encoding (default: utf-8)
                    - preserved_template_key: Key for template path (default: TEMPLATE_PATH)
                    - preserved_children_key: Key for children (default: CHILDREN_PATH)
        """
        if "root_path" not in config:
            raise ValueError("Missing required field 'root_path'")

        root_path = Path(config["root_path"])
        if not root_path.exists():
            raise ValueError(f"root_path {root_path} does not exist")

        return cls(
            root_path=root_path,
            encoding=config.get("encoding", "utf-8"),
            preserved_template_key=config.get(
                "preserved_template_key", "TEMPLATE_PATH"
            ),
            preserved_children_key=config.get(
                "preserved_children_key", "CHILDREN_PATH"
            ),
        )


class YamlDataTreeHandler:
    """Handler for YAML data trees that implement DataHandler protocol"""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the handler with configuration"""
        self.config = YamlConfig.validate(config)
        # Initialize the data tree with a root node
        self.data_tree: DataNode = DataNode(data=None, name=self.config.root_path.name)
        # Load the YAML file and initialize the data tree
        self.data_tree_init()
        
    @property
    def preserved_template_key(self) -> str:
        """Get preserved template key from config"""
        return self.config.preserved_template_key

    @property
    def preserved_children_key(self) -> str:
        """Get preserved children key from config"""
        return self.config.preserved_children_key

    def data_tree_init(self) -> None:
        """Initialize the data tree from the YAML file"""
        yaml_data = self.load_yaml_file(str(self.config.root_path))
        if yaml_data:
            self.data_tree.data = yaml_data
            # Here you would typically parse the YAML data and build the tree structure
            # For simplicity, we assume the root node contains the entire YAML data
            # In practice, you would traverse and create child nodes as needed
            
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

    def get_data(self) -> Iterator[Dict[str, Any]]:
        """Get data iterator, yielding each node's data from the tree"""
        # This is a placeholder implementation
        # In practice, this should traverse the data tree and yield each node's data
        
        data = self.load_yaml_file(str(self.config.root_path))
        yield data
