import os
import yaml
import shutil

class TemplateManager:
    def __init__(self, template_dir=None):
        self.template_dir = template_dir
    
    def set_template_dir(self, dir_path):
        """设置模板目录"""
        self.template_dir = dir_path
    
    def get_templates(self):
        """获取所有可用的模板"""
        templates = []
        if not self.template_dir or not os.path.exists(self.template_dir):
            return templates
            
        for root, dirs, files in os.walk(self.template_dir):
            for file in files:
                if file.endswith('.yaml'):
                    templates.append(os.path.join(root, file))
        return templates
    
    def create_instance(self, template_path, target_dir, target_name):
        """从模板创建新实例"""
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")
            
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        target_path = os.path.join(target_dir, target_name)
        shutil.copy2(template_path, target_path)
        
        return target_path
    
    def load_yaml(self, file_path):
        """加载YAML文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise Exception(f"Error loading YAML file: {e}")
    
    def save_yaml(self, file_path, content):
        """保存YAML文件内容"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(content, f, allow_unicode=True)
        except Exception as e:
            raise Exception(f"Error saving YAML file: {e}")
