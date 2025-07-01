import yaml
from typing import Optional, List, Dict, Any, Iterator, cast
from dataclasses import dataclass
from pathlib import Path

from .errors import (
    YamlError,
    YamlConfigError, 
    YamlPathError, 
    YamlLoadError, 
    YamlStructureError
)
from ..node.data_node import DataNode
from ..node.file_node import DirectoryNode, FileNode


@dataclass
class YamlConfig:
    """YAML configuration with preserved keys for template and children paths"""

    root_path: Path
    file_pattern: List[str]
    encoding: str = "utf-8"
    # These keys are moved from DataDrivenGeneratorConfig since they are specific to YAML data handling
    preserved_template_key: str = "TEMPLATE_PATH"
    preserved_children_key: str = "CHILDREN_PATH"
    max_depth: int = 1000  # Default maximum depth for recursion

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
            raise YamlConfigError("Missing required field 'root_path'")

        root_path = Path(config["root_path"])
        if not root_path.exists():
            raise YamlPathError(f"root_path {root_path} does not exist", str(root_path))

        return cls(
            root_path=root_path,
            file_pattern=config.get("file_pattern", ["*.yaml"]),
            encoding=config.get("encoding", "utf-8"),
            preserved_template_key=config.get(
                "preserved_template_key", "TEMPLATE_PATH"
            ),
            preserved_children_key=config.get(
                "preserved_children_key", "CHILDREN_PATH"
            ),
        )


class YamlFileHandler:
    @staticmethod
    def load_yaml_file(yaml_path: str) -> dict:
        """Load a YAML file and return its contents as a dictionary."""
        try:
            with open(yaml_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data is None:
                    return {}
                return data
        except (IOError, yaml.YAMLError) as e:
            raise YamlLoadError(str(e), yaml_path)


class YamlDataTreeHandler:
    """Handler for YAML data trees that implement DataHandler protocol"""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the handler with configuration"""
        self.config = YamlConfig.validate(config)
        self._node_paths: List[str] = []  # Track node paths to detect cycles

        # Initialize the yaml file tree with a root node
        self.file_tree: DirectoryNode = DirectoryNode(
            dir_name=str(self.config.root_path)
        )
        self.file_tree_init()
        # Initialize the data tree with a root node
        self.data_tree_list: List[DataNode] = []
        self.data_tree_list_init()

    @property
    def preserved_template_key(self) -> str:
        """Get preserved template key from config"""
        return self.config.preserved_template_key

    @property
    def preserved_children_key(self) -> str:
        """Get preserved children key from config"""
        return self.config.preserved_children_key

    def get_absolute_path(self, node: DataNode) -> str:
        """Get the absolute path of the root YAML file"""
        return str(self.config.root_path.resolve()) + node._node.get_absolute_path()

    def file_tree_init(self) -> None:
        """Initialize the file tree from the YAML file"""
        self.file_tree.build_tree(
            str(self.config.root_path), patterns=self.config.file_pattern
        )

    def _data_node_create(self, file_node: FileNode, depth: int) -> DataNode:
        if depth > self.config.max_depth:
            raise YamlStructureError.max_depth_exceeded(
                self.config.max_depth, file_node.name
            )

        file_system_path: str = self.file_tree.name + file_node.get_absolute_path()
        data = YamlFileHandler.load_yaml_file(file_system_path)
        if data:
            data_node = DataNode(data=data, name=file_node.name)
            if self.config.preserved_template_key not in data:
                raise YamlStructureError.missing_key(
                    self.config.preserved_template_key, file_system_path
                )
            elif self.config.preserved_children_key not in data:
                raise YamlStructureError.missing_key(
                    self.config.preserved_children_key, file_system_path
                )

            # Process child nodes
            children_path = data_node.data[self.config.preserved_children_key]
            if children_path == "":  # Handle empty string as empty list
                children_path = []

            if isinstance(children_path, list):
                # Create child nodes for each pattern in the list
                for pattern in children_path:
                    if not pattern:  # Skip empty patterns
                        continue
                    if file_node.parent:
                        matching_files = cast(
                            DirectoryNode, file_node.parent
                        ).find_nodes_by_path(pattern)
                        for matching_file in matching_files:
                            if isinstance(matching_file, FileNode):
                                try:
                                    child_node = self._data_node_create(
                                        matching_file, depth + 1
                                    )
                                    data_node._node.add_child(child_node._node)
                                    if child_node not in self.data_tree_list:
                                        self.data_tree_list.append(child_node)
                                except YamlError as e:
                                    # Re-raise with context about which child failed
                                    raise YamlStructureError(
                                        e.error_type,
                                        f"Error processing child {matching_file.name}: {str(e)}",
                                        str(matching_file.get_absolute_path())
                                    ) from e
            elif (
                isinstance(children_path, str) and children_path
            ):  # Only process non-empty string
                # Create child nodes using the single pattern
                if file_node.parent:
                    matching_files = cast(
                        DirectoryNode, file_node.parent
                    ).find_nodes_by_path(children_path)
                    for matching_file in matching_files:
                        if isinstance(matching_file, FileNode):
                            try:
                                child_node = self._data_node_create(
                                    matching_file, depth + 1
                                )
                                data_node._node.add_child(child_node._node)
                                if child_node not in self.data_tree_list:
                                    self.data_tree_list.append(child_node)
                            except YamlError as e:
                                # Re-raise with context about which child failed
                                raise YamlStructureError(
                                    e.error_type,
                                    f"Error processing child {matching_file.name}: {str(e)}",
                                    str(matching_file.get_absolute_path())
                                ) from e
        else:
            raise YamlLoadError(f"Failed to load data", file_system_path)
        return data_node

    def data_tree_list_init(self) -> None:
        """Initialize the data tree list from the YAML file"""
        # Reset state
        self._node_paths = []
        self.data_tree_list = []

        if len(self.file_tree.children) == 0:
            return

        try:
            # Process each YAML file in the tree
            for child in self.file_tree.children:
                if isinstance(child, FileNode):
                    try:
                        data_node = self._data_node_create(child, 0)
                        self.data_tree_list.append(data_node)
                    except YamlError as e:
                        # Re-raise all YAML errors as they are already properly handled
                        raise
        except YamlError as e:
            # Clear state on errors
            self._node_paths = []
            self.data_tree_list = []
            raise
