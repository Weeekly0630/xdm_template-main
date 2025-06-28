from typing import Optional, List, Dict
import sys
import os
# Ensure the tools directory is in sys.path for relative import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from xdm_typedef import YamlTreeHandler, XdmListNode, JinjaEnvironment

if __name__ == "__main__":
    yaml_root_abs_path: Optional[str] = rf"U:\Users\Enlink\Documents\code\python\Xdm\IPC"
    
    try:
        # Initialize Jinja environment
        jinja_env = JinjaEnvironment(
            template_dir=rf"U:\Users\Enlink\Documents\code\python\Xdm\template"
        )

        # Process YAML files and build node tree
        # nodes = analyze_yaml_files(yaml_root_abs_path)
        
        yaml_tree_handler = YamlTreeHandler(yaml_root_abs_path)
        nodes = yaml_tree_handler.generate()
        
        end_string = ""
        # Render each root node
        for root in nodes:
            try:
                rendered_output = jinja_env.render_node(root)
                print("Successfully rendered output:")

                end_string += (rendered_output)

            except RuntimeError as e:
                print(f"Rendering error: {str(e)}")
        print("======OUTPUT======")
        print(end_string)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")