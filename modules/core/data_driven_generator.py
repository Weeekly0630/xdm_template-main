"""Data-driven generator module for Jinja Template"""

from enum import Enum
from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass
from ..jinja.jinja_handler import JinjaTemplateHandler
from ..yaml.yaml_handler import YamlDataTreeHandler

class DataDrivenGeneratorError(Exception):
    """Custom exception for DataDrivenGenerator errors"""
    pass

class DataType(Enum):
    """Enum for data types"""

    YAML = "yaml"


class TemplateType(Enum):
    """Enum for template types"""

    JINJA = "jinja"


@dataclass
class DataDrivenGeneratorConfig:
    """Configuration for the DataDrivenGenerator"""

    data_type: DataType
    data_config: Dict[str, Any]
    template_type: TemplateType
    template_config: Dict[str, Any]
    preserved_template_key: str = (
        "TEMPLATE_PATH"  # Key to preserve the template path in the data context
    )
    preserved_children_key: str = (
        "CHILDREN_PATH"  # Key to preserve the children in the data context
    )


class DataDrivenGenerator:
    """Data-driven generator class
    This class is responsible for generating data-driven templates based on provided data.
    """

    def __init__(self, config: DataDrivenGeneratorConfig) -> None:
        self.data_handler: Any
        self.data_init(config.data_type, self.data_handler, config.data_config)
        self.template_handler: Any
        self.template_init(
            config.template_type, self.template_handler, config.template_config
        )

    """
    Initialize the data based on the data type.
    """

    @staticmethod
    def data_init(
        data_type: DataType, data_handler: Any, data_config: Dict[str, Any]
    ) -> None:
        """Initialize the data based on the data type."""
        data_init_handler = getattr(
            DataDrivenGenerator, f"{data_type.value}_data_init", None
        )
        if data_init_handler and callable(data_init_handler):
            data_init_handler(data_handler)
        else:
            raise NotImplementedError(
                f"Data initialization for {data_type.value} is not implemented."
            )

    @staticmethod
    def yaml_data_init(data_handler: Any, data_config: Dict[str, Any]) -> None:
        """Initialize the data for the generator.
        This method should be overridden by subclasses to provide specific data initialization logic.
        """
        data_handler = YamlDataTreeHandler(data_config)

        if not data_handler:
            raise ValueError(
                "Failed to initialize YAML data handler with provided config."
            )

    """
    Initialize the template based on the template type.
    """

    @staticmethod
    def template_init(
        template_type: TemplateType,
        template_handler: Any,
        template_config: Dict[str, Any],
    ) -> None:
        """Initialize the template based on the template type."""
        template_handler = getattr(
            DataDrivenGenerator, f"{template_type.value}_template_init", None
        )
        if template_handler and callable(template_handler):
            template_handler(template_config)
        else:
            raise NotImplementedError(
                f"Template initialization for {template_type.value} is not implemented."
            )

    @staticmethod
    def jinja_template_init(
        template_handler: Any, template_config: Dict[str, Any]
    ) -> None:
        """Initialize the Jinja template.
        This method should be overridden by subclasses to provide specific template initialization logic.
        """
        template_handler = JinjaTemplateHandler(template_config)

    def render(self) -> str:
        """Render the template with the data."""
        result: Optional[str] = ""

        # Get the data from the data handler
        if not hasattr(self.data_handler, "get_data"):
            raise ValueError("Data handler is not initialized.")

        for data_context in self.data_handler.get_data():
            # Validate the data context
            if not isinstance(data_context, dict):
                raise ValueError(
                    "Data context must be a dictionary containing the template path."
                )

            # Check if the preserved template key exists in the data context
            if self.data_handler.preserved_template_key not in data_context:
                raise ValueError(
                    f"Data context must contain the key '{self.data_handler.preserved_template_key}'"
                )

            # Get the template path from the data context
            template_path: str = data_context.get(
                self.data_handler.preserved_template_key, ""
            )

            # render the template using the template handler
            if not hasattr(self.template_handler, "render_template"):
                raise ValueError("Template handler is not initialized.")
            result = self.template_handler.render_template(template_path, data_context)
            if result is None:
                raise ValueError(
                    f"Failed to render template '{template_path}' with the provided data context."
                )
            
            # Set 
            self.data_handler.

        return str(result)
