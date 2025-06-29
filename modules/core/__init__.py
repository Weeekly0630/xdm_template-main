from enum import Enum
from typing import Any, Dict, Optional, Protocol, Iterator, runtime_checkable

class GeneratorErrorType(Enum):
    """Error types for data driven generator"""
    DATA_INIT_ERROR = "Data initialization error"
    TEMPLATE_INIT_ERROR = "Template initialization error"
    RENDER_ERROR = "Render error"
    VALIDATION_ERROR = "Validation error"

class GeneratorError(Exception):
    """Unified error class for all generator related errors"""
    def __init__(self, error_type: GeneratorErrorType, message: str):
        self.error_type = error_type
        self.message = message
        super().__init__(f"{error_type.value}: {message}")

@runtime_checkable
class DataHandler(Protocol):
    """Protocol defining required methods for data handlers"""
    def get_data(self) -> Iterator[Dict[str, Any]]:
        """Get data iterator"""
        ...

    @property
    def preserved_template_key(self) -> str:
        """Get preserved template key"""
        ...

    @property
    def preserved_children_key(self) -> str:
        """Get preserved children key"""
        ...

@runtime_checkable
class TemplateHandler(Protocol):
    """Protocol defining required methods for template handlers"""
    def render_template(self, template_path: str, context: Dict[str, Any]) -> Optional[str]:
        """Render template with given context"""
        ...

def validate_data_handler(data_handler: Any) -> None:
    """Validate data handler initialization"""
    if not data_handler:
        raise GeneratorError(
            GeneratorErrorType.DATA_INIT_ERROR,
            "Failed to initialize data handler with provided config."
        )
    if not hasattr(data_handler, "get_data"):
        raise GeneratorError(
            GeneratorErrorType.DATA_INIT_ERROR,
            "Data handler is not initialized."
        )

def validate_template_handler(template_handler: Any) -> None:
    """Validate template handler initialization"""
    if not template_handler:
        raise GeneratorError(
            GeneratorErrorType.TEMPLATE_INIT_ERROR,
            "Failed to initialize template handler with provided config."
        )
    if not hasattr(template_handler, "render_template"):
        raise GeneratorError(
            GeneratorErrorType.TEMPLATE_INIT_ERROR,
            "Template handler is not initialized."
        )

def validate_data_context(data_context: Any, preserved_template_key: str) -> None:
    """Validate data context for rendering"""
    if not isinstance(data_context, dict):
        raise GeneratorError(
            GeneratorErrorType.VALIDATION_ERROR,
            "Data context must be a dictionary containing the template path."
        )
    if preserved_template_key not in data_context:
        raise GeneratorError(
            GeneratorErrorType.VALIDATION_ERROR,
            f"Data context must contain the key '{preserved_template_key}'"
        )

def validate_render_result(result: Optional[str], template_path: str) -> None:
    """Validate render result"""
    if result is None:
        raise GeneratorError(
            GeneratorErrorType.RENDER_ERROR,
            f"Failed to render template '{template_path}' with the provided data context."
        )
