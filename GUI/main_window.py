import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import os
import yaml
from .template_manager import TemplateManager

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("YAML Template Manager")
        self.root.geometry("800x600")
        
        # 创建主布局
        self.create_layout()
        
        # 当前选择的模板目录
        self.template_dir = None
        self.current_file = None
        self.template_manager = TemplateManager()
    
    def create_layout(self):
        # 创建左右分隔的布局
        self.paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)
        
        # 左侧：文件树
        self.left_frame = ttk.Frame(self.paned)
        self.tree = ttk.Treeview(self.left_frame)
        self.tree.bind('<<TreeviewSelect>>', self.on_select_file)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.paned.add(self.left_frame)
        
        # 右侧：控制面板和内容区
        self.right_frame = ttk.Frame(self.paned)
        
        # 控制面板
        self.control_frame = ttk.Frame(self.right_frame)
        self.open_btn = ttk.Button(self.control_frame, text="打开文件夹", command=self.open_folder)
        self.open_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.create_btn = ttk.Button(self.control_frame, text="创建模板", command=self.create_template)
        self.create_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.control_frame.pack(fill=tk.X)
        
        # 内容区域
        self.content_frame = ttk.Frame(self.right_frame)
        
        # 编辑器工具栏
        self.editor_toolbar = ttk.Frame(self.content_frame)
        self.save_btn = ttk.Button(self.editor_toolbar, text="保存", command=self.save_file)
        self.save_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.editor_toolbar.pack(fill=tk.X)
        
        # 文本编辑器
        self.text_editor = tk.Text(self.content_frame)
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        self.paned.add(self.right_frame)
    
    def open_folder(self):
        """打开文件夹并显示文件树"""
        folder = filedialog.askdirectory()
        if folder:
            self.template_dir = folder
            self.template_manager.set_template_dir(folder)
            self.refresh_tree()
    
    def refresh_tree(self):
        """刷新文件树显示"""
        # 清空现有项目
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if not self.template_dir:
            return
            
        # 添加根目录
        root_node = self.tree.insert('', 'end', text=os.path.basename(self.template_dir), open=True)
        self.populate_tree(root_node, self.template_dir)
    
    def populate_tree(self, parent, path):
        """递归填充文件树"""
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path) and item.endswith('.yaml'):
                    self.tree.insert(parent, 'end', text=item, values=(item_path,))
                elif os.path.isdir(item_path):
                    node = self.tree.insert(parent, 'end', text=item, open=False)
                    self.populate_tree(node, item_path)
        except Exception as e:
            print(f"Error populating tree: {e}")
    
    def create_template(self):
        """创建新的模板实例"""
        if not self.template_dir:
            messagebox.showwarning("警告", "请先选择模板目录")
            return
        
        # 获取可用模板列表
        templates = self.template_manager.get_templates()
        if not templates:
            messagebox.showinfo("提示", "当前目录下没有可用的模板")
            return
        
        # 创建模板选择对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("选择模板")
        dialog.geometry("400x300")
        
        # 添加模板列表
        frame = ttk.Frame(dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 模板列表
        template_var = tk.StringVar()
        for template in templates:
            ttk.Radiobutton(frame, text=os.path.basename(template),
                          variable=template_var, value=template).pack(anchor=tk.W)
        
        # 目标文件名输入
        name_frame = ttk.Frame(frame)
        name_frame.pack(fill=tk.X, pady=10)
        ttk.Label(name_frame, text="文件名:").pack(side=tk.LEFT)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=name_var)
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        def on_create():
            template_path = template_var.get()
            if not template_path:
                messagebox.showwarning("警告", "请选择一个模板")
                return
                
            target_name = name_var.get()
            if not target_name:
                messagebox.showwarning("警告", "请输入文件名")
                return
                
            if not target_name.endswith('.yaml'):
                target_name += '.yaml'
                
            try:
                # 创建模板实例
                new_file = self.template_manager.create_instance(
                    template_path, self.template_dir, target_name)
                dialog.destroy()
                self.refresh_tree()
                messagebox.showinfo("成功", f"已创建模板实例: {target_name}")
            except Exception as e:
                messagebox.showerror("错误", str(e))
        
        # 确认按钮
        ttk.Button(frame, text="创建", command=on_create).pack(pady=10)

    def on_select_file(self, event):
        """当在树形视图中选择文件时触发"""
        selection = self.tree.selection()
        if not selection:
            return
            
        item = selection[0]
        values = self.tree.item(item)['values']
        if not values:  # 可能是目录
            return
            
        file_path = values[0]
        if not os.path.isfile(file_path):
            return
            
        try:
            # 加载并显示YAML内容
            content = self.template_manager.load_yaml(file_path)
            self.current_file = file_path
            self.text_editor.delete('1.0', tk.END)
            self.text_editor.insert('1.0', yaml.dump(content, allow_unicode=True))
        except Exception as e:
            messagebox.showerror("错误", f"无法加载文件: {str(e)}")
    
    def save_file(self):
        """保存当前编辑的文件"""
        if not self.current_file:
            messagebox.showwarning("警告", "没有选择文件")
            return
            
        try:
            # 获取编辑器内容并解析YAML
            content = self.text_editor.get('1.0', tk.END)
            yaml_content = yaml.safe_load(content)
            
            # 保存文件
            self.template_manager.save_yaml(self.current_file, yaml_content)
            messagebox.showinfo("成功", "文件已保存")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {str(e)}")

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
