import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from tools import process_yaml_to_xdm

if __name__ == "__main__":
    try:
        # Set up paths
        yaml_root_path = str(project_root / "DIO")
        template_dir = str(project_root / "template")

        # Process YAML to XDM with project root
        result = process_yaml_to_xdm(
            yaml_root_path=yaml_root_path,
            template_dir=template_dir,
            project_root=str(project_root)
        )

        # Write output to file
        print("======OUTPUT======")
        with open("output.xdm", "w", encoding="utf-8") as f:
            f.write(result)
        print("Output written to file: output.xdm")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
