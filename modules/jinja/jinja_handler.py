from jinja2 import Environment, FileSystemLoader, Template
from typing import Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path


@dataclass
class JinjaConfig:
    template_type: str  # "file" or "string"
    # template_content: str  # 当type为string时的模板内容
    template_dir: Optional[Path] = None  # 当type为file时的模板目录
    auto_escape: bool = True
    encoding: str = "utf-8"

    @classmethod
    def validate(cls, config: Dict[str, Any]) -> "JinjaConfig":
        """验证配置并返回配置对象"""
        if "template_type" not in config:
            raise ValueError("Missing required field 'template_type'")

        template_type = config["template_type"]
        if template_type not in ["file", "string"]:
            raise ValueError("template_type must be 'file' or 'string'")

        if template_type == "file":
            if "template_dir" not in config:
                raise ValueError("template_dir is required for file template")
            template_dir = Path(config["template_dir"])
            if not template_dir.exists():
                raise ValueError(f"template_dir {template_dir} does not exist")

        if "template_content" not in config:
            raise ValueError("Missing required field 'template_content'")

        return cls(
            template_type=template_type,
            # template_content=config["template_content"],
            template_dir=(
                Path(config["template_dir"]) if "template_dir" in config else None
            ),
            auto_escape=config.get("auto_escape", True),
            encoding=config.get("encoding", "utf-8"),
        )


class JinjaTemplateHandler:
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the Jinja environment with the specified template directory."""
        self.config = JinjaConfig.validate(config)

        if self.config.template_type == "file":
            self.env = Environment(
                loader=(
                    FileSystemLoader(str(self.config.template_dir))
                    if str(self.config.template_dir)
                    else None
                ),
                autoescape=True,
            )
        else:
            raise ValueError(
                "JinjaTemplateHandler only supports 'file' template type for now."
            )

    def _load_template_from_file(self, template_name: str) -> Optional[Template]:
        """Load a Jinja template from a file."""
        try:
            return self.env.get_template(template_name)
        except Exception as e:
            print(f"Error loading template {template_name}: {e}")
            return None

    def render_template(
        self, template_name: str, context: Dict[str, Any]
    ) -> Optional[str]:
        """Render a Jinja template with the provided context."""
        template = self._load_template_from_file(template_name)
        if template:
            try:
                return template.render(context)
            except Exception as e:
                print(f"Error rendering template {template_name}: {e}")
                return None
        return None
