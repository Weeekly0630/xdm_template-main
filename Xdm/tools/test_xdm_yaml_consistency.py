import yaml
import os
import sys

# Ensure the tools directory is in sys.path for relative import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from xdm_typedef import XdmListNode, JinjaEnvironment


def test_template_rendering(xdm_path, jinja_env: JinjaEnvironment) -> str:
    output_string: str = ""
    """测试模板渲染，检查是否缺少必要变量"""
    print(f"\nTesting template: {xdm_path}")

    # 构造对应的 YAML 文件路径
    yaml_path = jinja_env.template_dir + "/" + str(xdm_path).replace(".xdm", ".yaml")
    print(f"Looking for YAML file: {yaml_path}")

    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            yaml_content = f.read()
            print("✓ YAML file loaded successfully")
    except FileNotFoundError:
        print(f"Error: YAML file not found: {yaml_path}")
        return False
    except Exception as e:
        print(f"Error reading YAML file: {e}")
        return False

    # 加载 YAML 配置
    try:
        yaml_data = yaml.safe_load(yaml_content)
        if yaml_data is None:
            yaml_data = {}
        print(f"Loaded YAML data: {yaml_data}")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML content: {e}")
        return False
    try:
        output_string = jinja_env.render_node(
            XdmListNode(
                template_name=xdm_path,
                usr_data=yaml_data,
                children_text="",
                children=[],  # 假设没有子节点，实际使用时可以根据需要添加
            )
        )
    except RuntimeError as e:
        print(f"Error rendering template: {e}")
        output_string = ""
    return output_string


def main():
    # 测试单个文件
    xdm_path = rf"var/v_ctr.xdm"

    jinja_env = JinjaEnvironment(
        template_dir=rf"U:\Users\Enlink\Documents\code\python\Xdm\template"
    )

    result = test_template_rendering(xdm_path, jinja_env)
    print("======OUTPUT======")
    print(result)
    print("===================")
    
if __name__ == "__main__":
    main()

