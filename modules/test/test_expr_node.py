import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from modules.node.expr_node import ExprASTParser, ExprPrintVistor

# 示例输入数据
sample_data = {
    "complex_xpath": {
        "type": "xpath",
        "args": ["parent", "child[@id='123']"],
    },
    "function_with_args": {"type": "function", "args": ["node:value", "parent/node"]},
    "node_functions": {
        "type": "expression",
        "operator": "and",
        "args": [
            {"type": "function", "args": ["node:exists", "CanControllerRef"]},
            {"type": "function", "args": ["node:value", "."]},
        ],
    },
}

parser = ExprASTParser()

# 解析为AST
ast_nodes = {}
for name, data in sample_data.items():
    ast_nodes[name] = parser.parse(data)

# 打印AST
printer = ExprPrintVistor()
for name, node in ast_nodes.items():
    print(f"{name}: {node.accept(printer)}")
