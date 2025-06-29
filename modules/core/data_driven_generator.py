"""Data-driven generator module for Jinja Template"""

from enum import Enum
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from . import (
    GeneratorError,
    GeneratorErrorType,
    DataHandler,
    TemplateHandler,
    validate_data_handler,
    validate_template_handler,
    validate_data_context,
    validate_render_result
)
from ..jinja.jinja_handler import JinjaTemplateHandler
from ..yaml.yaml_handler import YamlDataTreeHandler

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

class DataDrivenGenerator:
    """Data-driven generator class
    This class is responsible for generating data-driven templates based on provided data.
    """

    def __init__(self, config: DataDrivenGeneratorConfig) -> None:
        """Initialize the generator with configuration

        Note on typing:
        self.data_handler and self.template_handler are initialized as None
        but will be set to proper handlers in data_init and template_init.
        The type hints Optional[DataHandler] and Optional[TemplateHandler] tell
        Python these variables can be None or their respective handler types.
        """
        self.data_handler: Optional[DataHandler] = None
        self.template_handler: Optional[TemplateHandler] = None
        self.config = config
        self.data_init(config.data_type, config.data_config)
        self.template_init(config.template_type, config.template_config)

    def data_init(self, data_type: DataType, data_config: Dict[str, Any]) -> None:
        """Initialize the data based on the data type."""
        data_init_handler = getattr(self, f"{data_type.value}_data_init", None)
        if data_init_handler and callable(data_init_handler):
            data_init_handler(data_config)
        else:
            raise GeneratorError(
                GeneratorErrorType.DATA_INIT_ERROR,
                f"Data initialization for {data_type.value} is not implemented."
            )

    def yaml_data_init(self, data_config: Dict[str, Any]) -> None:
        """Initialize the YAML data handler"""
        self.data_handler = YamlDataTreeHandler(data_config)
        validate_data_handler(self.data_handler)

    def template_init(self, template_type: TemplateType, template_config: Dict[str, Any]) -> None:
        """Initialize the template based on the template type."""
        template_init_handler = getattr(self, f"{template_type.value}_template_init", None)
        if template_init_handler and callable(template_init_handler):
            template_init_handler(template_config)
        else:
            raise GeneratorError(
                GeneratorErrorType.TEMPLATE_INIT_ERROR,
                f"Template initialization for {template_type.value} is not implemented."
            )

    def jinja_template_init(self, template_config: Dict[str, Any]) -> None:
        """Initialize the Jinja template handler"""
        self.template_handler = JinjaTemplateHandler(template_config)
        validate_template_handler(self.template_handler)

    def render(self) -> str:
        """Render the template with the data.
        
        Note on isinstance checks:
        Even though data_handler and template_handler are initialized in __init__,
        Python's type checker needs runtime checks to verify they are the correct types
        and not None. This is because:
        1. The handlers are declared as Optional[Type], meaning they could be None
        2. Python's type system is static at compile time but dynamic at runtime
        3. Without these checks, we can't guarantee the type safety of method calls
        """
        # Runtime type checks required for type safety
        if not isinstance(self.data_handler, DataHandler):
            raise GeneratorError(
                GeneratorErrorType.DATA_INIT_ERROR,
                "Data handler not properly initialized"
            )
        if not isinstance(self.template_handler, TemplateHandler):
            raise GeneratorError(
                GeneratorErrorType.TEMPLATE_INIT_ERROR,
                "Template handler not properly initialized"
            )

        result: Optional[str] = ""

        for data_context in self.data_handler.get_data():
            # Validate the data context
            validate_data_context(data_context, self.data_handler.preserved_template_key)

            # Get the template path from the data context
            template_path: str = data_context.get(self.data_handler.preserved_template_key, "")

            # Render the template using the template handler
            result = self.template_handler.render_template(template_path, data_context)
            validate_render_result(result, template_path)

        return str(result)
