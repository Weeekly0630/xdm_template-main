import yaml
from typing import Dict, Any, List, Union, Optional
from pathlib import Path
import sys
import os

from .xdm_expr_typedef import (
    XdmElement,
    XdmElementType,
    XdmExpression,
    XdmXPathValue,
    XdmFunctionValue,
    XdmOperator,
    XdmFunctionLibrary,
)

class XdmElementLoader:
    """用于从YAML文件加载和构建XDM元素的加载器。

    支持加载以下类型的元素：
    - xpath: XPath表达式
    - function: 函数调用
    - expression: 复合表达式
    """

    # 操作符字符串到枚举值的映射
    OPERATOR_MAP = {
        # 比较运算符
        "none": XdmOperator.NONE,
        "equal": XdmOperator.EQUAL,
        "not_equal": XdmOperator.NOT_EQUAL,
        "less_than": XdmOperator.LESS_THAN,
        "less_than_or_equal": XdmOperator.LESS_THAN_OR_EQUAL,
        "greater_than": XdmOperator.GREATER_THAN,
        "greater_than_or_equal": XdmOperator.GREATER_THAN_OR_EQUAL,
        
        # 逻辑运算符
        "and": XdmOperator.AND,
        "or": XdmOperator.OR,
        "not": XdmOperator.NOT,
    }

    TYPE_MAP = {
        "xpath": XdmXPathValue,
        "function": XdmFunctionValue,
        "expression": XdmExpression,
    }
    def __init__(self):
        self.function_lib = XdmFunctionLibrary()
        self.root_node = None
        
    def set_root_node(self, root_node):
        """设置根节点"""
        self.root_node = root_node
        self.function_lib.root_node = root_node
        
    def set_current_node(self, node):
        """设置当前处理节点上下文"""
        self.function_lib.set_current_node(node)

    def _parse_operator(self, operator_str: str) -> XdmOperator:
        """将YAML中的操作符字符串转换为XdmOperator枚举值。"""
        if operator_str not in self.OPERATOR_MAP:
            supported_operators = ", ".join(f"'{op}'" for op in self.OPERATOR_MAP.keys())
            raise ValueError(
                f"Unknown operator: '{operator_str}'. "
                f"Supported operators are: [{supported_operators}]"
            )
        return self.OPERATOR_MAP[operator_str]

    def _build_value(self, value_data: Union[Dict[str, Any], str, List[Any], None]) -> Optional[XdmElement]:
        """根据YAML数据构建XDM元素。"""
        if value_data is None:
            return None
        
        # 处理简单字符串值
        if isinstance(value_data, str):
            return XdmElement(value_data)
            
        # 处理列表值 - 作为参数列表
        if isinstance(value_data, list):
            return XdmElement([
                self._build_value(item) if isinstance(item, (dict, list)) else item 
                for item in value_data
            ])

        # 处理字典值
        if not isinstance(value_data, dict) or "type" not in value_data:
            raise ValueError(f"Invalid value data: {value_data}")

        value_type = value_data["type"]
        
        if value_type == "expression":
            # 处理表达式 - 参数列表格式，第一个是操作符，后面是操作数
            if "operator" not in value_data:
                raise ValueError("Expression must specify an operator")
                
            operator = self._parse_operator(value_data["operator"])
            operands = [
                self._build_value(item) if isinstance(item, (dict, list)) else item
                for item in value_data.get("args", [])
            ]
            return XdmExpression([operator] + operands)
        
        elif value_type == "xpath":
            # 处理XPath值 - 使用参数列表格式
            args = [
                self._build_value(item) if isinstance(item, (dict, list)) else item
                for item in value_data.get("args", [])
            ]
            return XdmXPathValue(args)
            
        elif value_type == "function":
            # 处理函数调用 - 使用参数列表格式
            args = [
                self._build_value(item) if isinstance(item, (dict, list)) else item
                for item in value_data.get("args", [])
            ]
            return XdmFunctionValue(args, self.function_lib)
        
        else:
            raise ValueError(f"Unknown value type: {value_type}")

    def load_from_yaml(self, yaml_path: Union[str, Path], expr_name: str = None) -> Union[XdmElement, Dict[str, XdmElement]]:
        """从YAML文件加载并构建XdmExpression对象。

        Args:
            yaml_path: YAML文件路径
            expr_name: 表达式名称，如果指定则只加载该表达式，否则加载所有表达式

        Returns:
            如果指定expr_name，返回单个表达式
            如果未指定expr_name，返回所有表达式的字典
        """
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if "elements" not in data:
            raise ValueError("YAML must contain an 'elements' section")

        if expr_name is not None:
            if expr_name not in data["elements"]:
                raise ValueError(f"Element '{expr_name}' not found")
            return self._build_value(data["elements"][expr_name])
        
        # 加载所有元素
        result = {}
        failed = []
        for name, elem_data in data["elements"].items():
            try:
                result[name] = self._build_value(elem_data)
            except Exception as e:
                failed.append((name, str(e)))
                continue
        
        # 报告加载失败的表达式
        if failed:
            print("\nWarning: Some elements failed to load:")
            for name, error in failed:
                print(f"  - {name}: {error}")
        
        return result

def main():
    """测试加载器的示例。"""
    try:
        print("\n" + "="*50)
        print("XDM Element Loader Test")
        print("="*50)
        
        loader = XdmElementLoader()

        # 显示函数库帮助信息
        # print("\nAvailable Functions:")
        # print("-" * 50)
        # print(loader.function_lib.get_function_help())

        # 显示具体函数的详细信息
        # for func_name in ["node:fallback", "text:match", "ecu:get"]:
        #     print("\nFunction Details:")
        #     print("-" * 50)
        #     print(loader.function_lib.get_function_help(func_name))

        print("\nLoading example expressions...")
        print("-" * 50)
        expressions = loader.load_from_yaml(rf"U:\Users\Enlink\Documents\code\python\Xdm\tools\expr\expr_example3.yaml")
        
        if expressions:
            print("\nSuccessfully loaded elements:")
            for name, expr in expressions.items():
                print(f"\n{name}:")
                print("-" * 30)
                print(f"Expression: {str(expr)}")
        else:
            print("\nNo valid expressions were loaded.")
        
        return 0
        
    except Exception as e:
        print("\nError loading expressions:")
        print(f"  {type(e).__name__}: {str(e)}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
