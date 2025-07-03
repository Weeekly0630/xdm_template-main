"""Example usage and test of DataDrivenGenerator with explanations of key Python concepts"""

import os
from pathlib import Path
from typing import Dict, Any

from ..core.data_driven_generator import (
    DataDrivenGenerator,
    DataDrivenGeneratorConfig,
    DataType,
    TemplateType,
)

def test_data_driven_generator():
    """Test the DataDrivenGenerator with example data and template"""
    
    # Create test directories if they don't exist
    current_dir = Path(__file__).parent
    data_dir = current_dir / "test_data"
    template_dir = current_dir / "test_templates"
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(template_dir, exist_ok=True)

    # Create a sample YAML data file
    yaml_content = """
    name: Test Project
    version: 1.0
    TEMPLATE_PATH: test_template.j2
    description: A test project
    items:
      - id: 1
        name: Item 1
      - id: 2
        name: Item 2
    """
    with open(data_dir / "test.yaml", "w") as f:
        f.write(yaml_content)

    # Create a sample Jinja template
    template_content = """
    # {{ name }} v{{ version }}

    {{ description }}

    ## Items
    {% for item in items %}
    * {{ item.name }} (ID: {{ item.id }})
    {% endfor %}
    """
    with open(template_dir / "test_template.j2", "w") as f:
        f.write(template_content)

    # --- Python Concept: Dictionary ---
    # Dictionaries are used to store key-value pairs
    # Here we create configuration dictionaries for our generator
    data_config: Dict[str, Any] = {
        "root_path": str(data_dir / "test.yaml"),
        "preserved_template_key": "TEMPLATE_PATH",
        "preserved_children_key": "CHILDREN_PATH"
    }

    template_config: Dict[str, Any] = {
        "template_type": "file",
        "template_dir": str(template_dir),
        "auto_escape": True
    }

    # --- Python Concept: Dataclass ---
    # DataDrivenGeneratorConfig is a @dataclass that provides a convenient way
    # to create classes that are primarily used to store data
    config = DataDrivenGeneratorConfig(
        data_type=DataType.YAML,        # Enum value
        data_config=data_config,        # Dictionary
        template_type=TemplateType.JINJA,# Enum value
        template_config=template_config  # Dictionary
    )

    # --- Python Concept: Class Instance ---
    # Create an instance of DataDrivenGenerator with our config
    generator = DataDrivenGenerator(config)

    # --- Python Concept: Method Call ---
    # Call the render method which will:
    # 1. Load data from the YAML file
    # 2. Use that data with the Jinja template
    # 3. Return the rendered result
    result = generator.render()

    print("\nGenerated output:")
    print(result)

    # --- Python Concept: Error Handling ---
    # The generator uses a unified error handling system through GeneratorError
    try:
        # Try with invalid config to demonstrate error handling
        bad_config = DataDrivenGeneratorConfig(
            data_type=DataType.YAML,
            data_config={"invalid": "config"},
            template_type=TemplateType.JINJA,
            template_config={"also": "invalid"}
        )
        bad_generator = DataDrivenGenerator(bad_config)
        bad_generator.render()
    except Exception as e:
        print(f"\nError handling example:")
        print(f"Caught error: {e}")

if __name__ == "__main__":
    # This ensures the test is only run when this file is executed directly
    test_data_driven_generator()
