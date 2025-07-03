import os
import sys
from pathlib import Path

# Add the parent directory to sys.path to import modules
current_dir = Path(__file__).parent
sys.path.append(str(current_dir.parent.parent))

from modules.core.data_driven_generator import DataDrivenGenerator, DataDrivenGeneratorConfig
from modules.core.types import DataHandlerType, TemplateHandlerType

def setup_example_files():
    """设置示例文件结构"""
    # 使用test/下的固定目录
    example_dir = current_dir / "test_data"
    example_dir.mkdir(exist_ok=True)
    
    # 创建配置文件
    config_dir = example_dir / "config"
    config_dir.mkdir(exist_ok=True)
    
    # 1. 创建根配置
    root_yaml = """
TEMPLATE_PATH: "root.j2"
CHILDREN_PATH: ["services/*.yaml"]
name: "System Configuration"
version: "2.0"
description: "System configuration with nested services"
subsystems: ["Web Service", "Database"]
"""
    with open(config_dir / "root.yaml", "w") as f:
        f.write(root_yaml.strip())
    
    # 2. 创建服务配置
    services_dir = config_dir / "services"
    services_dir.mkdir(exist_ok=True)
    
    # Web服务配置
    web_yaml = """
TEMPLATE_PATH: "web.j2"
CHILDREN_PATH: ["endpoints/*.yaml"]
name: "Web Service"
type: "http"
port: 8080
enabled: true
"""
    with open(services_dir / "web.yaml", "w") as f:
        f.write(web_yaml.strip())
    
    # 数据库服务配置
    db_yaml = """
TEMPLATE_PATH: "database.j2"
CHILDREN_PATH: []
name: "Database Service"
type: "postgresql"
port: 5432
enabled: true
max_connections: 100
"""
    with open(services_dir / "database.yaml", "w") as f:
        f.write(db_yaml.strip())
    
    # 3. 创建端点配置
    endpoints_dir = services_dir / "endpoints"
    endpoints_dir.mkdir(exist_ok=True)
    
    api_yaml = """
TEMPLATE_PATH: "endpoint.j2"
CHILDREN_PATH: []
name: "REST API"
path: "/api/v1"
methods: ["GET", "POST", "PUT"]
auth_required: true
"""
    with open(endpoints_dir / "api.yaml", "w") as f:
        f.write(api_yaml.strip())
    
    # 4. 创建模板文件
    template_dir = example_dir / "templates"
    template_dir.mkdir(exist_ok=True)
    
    # 根模板
    root_template = """
<?xml version="1.0" encoding="UTF-8"?>
<system>
    <info>
        <name>{{ name }}</name>
        <version>{{ version }}</version>
        <description>{{ description }}</description>
    </info>
    <subsystems>
        {% for system in subsystems %}
        <subsystem>{{ system }}</subsystem>
        {% endfor %}
    </subsystems>
    <services>
        {{ CHILDREN_CONTEXT }}
    </services>
</system>
"""
    with open(template_dir / "root.j2", "w") as f:
        f.write(root_template.strip())
    
    # Web服务模板
    web_template = """
<web-service>
    <info>
        <name>{{ name }}</name>
        <type>{{ type }}</type>
        <port>{{ port }}</port>
        <enabled>{{ enabled }}</enabled>
    </info>
    <endpoints>
        {{ CHILDREN_CONTEXT }}
    </endpoints>
</web-service>
"""
    with open(template_dir / "web.j2", "w") as f:
        f.write(web_template.strip())
    
    # 数据库服务模板
    db_template = """
<database-service>
    <info>
        <name>{{ name }}</name>
        <type>{{ type }}</type>
        <port>{{ port }}</port>
        <enabled>{{ enabled }}</enabled>
    </info>
    <config>
        <max-connections>{{ max_connections }}</max-connections>
    </config>
</database-service>
"""
    with open(template_dir / "database.j2", "w") as f:
        f.write(db_template.strip())
    
    # 端点模板
    endpoint_template = """
<endpoint>
    <name>{{ name }}</name>
    <path>{{ path }}</path>
    <methods>
        {% for method in methods %}
        <method>{{ method }}</method>
        {% endfor %}
    </methods>
    <auth-required>{{ auth_required }}</auth-required>
</endpoint>
"""
    with open(template_dir / "endpoint.j2", "w") as f:
        f.write(endpoint_template.strip())
        
    return example_dir

def demonstrate_generator():
    """演示DataDrivenGenerator的使用"""
    try:
        # 1. 准备示例文件
        example_dir = setup_example_files()
        
        # 2. 创建配置
        # 打印文件结构
        print("\n=== File Structure ===")
        print(f"Root dir: {example_dir}")
        print("Files:")
        for path in example_dir.rglob("*.*"):
            print(f"  {path.relative_to(example_dir)}")
            
        # 创建生成器配置
        config = DataDrivenGeneratorConfig(
            data_type=DataHandlerType.YAML_HANDLER,
            data_config={
                "root_path": str(example_dir / "config"),
                "file_pattern": ["*.yaml"]
            },
            template_type=TemplateHandlerType.JINJA_HANDLER,
            template_config={
                "template_dir": str(example_dir / "templates")
            }
        )
        
        # 3. 初始化生成器
        print("\n=== Initializing Generator ===")
        generator = DataDrivenGenerator(config)
        
        # 4. 渲染配置树
        print("\n=== Rendering Config Tree ===")
        try:
            result = generator.render("root.yaml")
            print("Result:")
            for key, content in result.items():
                print(f"\n=== {key} ===")
                print(content)
        except Exception as e:
            print(f"Render failed: {str(e)}")
            print(f"Exception type: {type(e).__name__}")
            raise
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    demonstrate_generator()
