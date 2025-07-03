"""
Expression Node Module
This module defines the `ExprNode` class, which represents an expression node in a tree structure.
"""

# from abc import ABC, abstractmethod

from enum import Enum, auto
from typing import Optional, List, Dict, Any, TypeVar, Iterable, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod
from ..user_func.func_handler import function_registry


class ExprNodeType(Enum):
    XPATH = auto()  # XPath表达式
    FUNCTION = auto()  # 函数调用
    EXPRESSION = auto()  # 复合表达式
    LITERAL = auto()  # 字面量常数


class ExprASTNode(ABC):
    """抽象语法树节点基类"""

    source: Optional[Dict]

    def __init__(self, source: Optional[Dict] = None):
        # 保留原始字典数据用于调试和错误报告
        self.source: Optional[Dict] = source

    @abstractmethod
    def accept(self, visitor: "ExprASTVisitor") -> Any:
        """访问者模式接受方法"""
        pass


class XPathNode(ExprASTNode):
    """XPath表达式节点"""

    def __init__(self, parts: List[ExprASTNode], source: Optional[Dict] = None):
        super().__init__(source)
        self.parts = parts  # 可以是字符串或嵌套节点

    def accept(self, visitor: "ExprASTVisitor") -> Any:
        return visitor.visit_xpath(self)


class FunctionNode(ExprASTNode):
    """函数调用节点"""

    def __init__(
        self, name: str, args: List[ExprASTNode], source: Optional[Dict] = None
    ):
        super().__init__(source)
        self.name = name
        self.args = args

    def accept(self, visitor: "ExprASTVisitor") -> Any:
        return visitor.visit_function(self)

    def execute(self, context: Optional[dict]) -> Any:
        """直接执行函数（用于解释器模式）"""
        # 解析参数值
        arg_values = [
            arg.execute(context) if isinstance(arg, FunctionNode) else arg
            for arg in self.args
        ]

        # 获取函数实现
        try:
            func = function_registry.get(self.name)
        except KeyError:
            # 如果未注册，尝试作为内置函数处理
            return f"{self.name}({', '.join(map(str, arg_values))})"

        # 执行函数
        return func(*arg_values, context=context)


class ExpressionOperator(Enum):
    """表达式操作符枚举"""

    ADD = auto()  # 加法
    SUBTRACT = auto()  # 减法
    MULTIPLY = auto()  # 乘法
    DIVIDE = auto()  # 除法
    CONCATENATE = auto()  # 字符串连接
    EQUALS = auto()  # 等于
    NOT_EQUALS = auto()  # 不等于
    LESS_THAN = auto()  # 小于
    GREATER_THAN = auto()  # 大于
    AND = auto()  # 与
    OR = auto()  # 或


@dataclass
class ExpressionOperatorInfo:
    Info = {}


class ExpressionNode(ExprASTNode):
    """表达式节点"""

    def __init__(
        self,
        operator: ExpressionOperator,
        operands: List[ExprASTNode],
        source: Optional[Dict] = None,
    ):
        super().__init__(source)
        self.operator = operator
        self.operands = operands

    def accept(self, visitor: "ExprASTVisitor") -> Any:
        return visitor.visit_expression(self)


class LiteralNode(ExprASTNode):
    """字面量节点（字符串、数字等）"""

    def __init__(
        self, value: Union[list, str, int, float, bool], source: Optional[Dict] = None
    ):
        super().__init__(source)
        self.value = value
        self.data_type = self._infer_type(value)

    def _infer_type(self, value) -> str:
        """推断字面量类型"""
        if isinstance(value, str):
            return "string"
        if isinstance(value, bool):
            return "boolean"
        if isinstance(value, (int, float)):
            return "number"
        elif isinstance(value, list):
            return "list"

        return "unknown"

    def accept(self, visitor: "ExprASTVisitor") -> Any:
        return visitor.visit_literal(self)


class ExprASTParser:
    """将字典解析为ExprAST树"""

    def parse(self, data: Union[Dict, list, str, int, float, bool]) -> ExprASTNode:
        """
        解析入口点，处理各种输入类型
        """
        if isinstance(data, dict):
            return self._parse_dict(data)
        else:
            return LiteralNode(data)

    def _parse_dict(self, data: Dict) -> ExprASTNode:
        """处理字典类型节点"""
        node_type = data.get("type")

        if node_type == "xpath":
            return self._parse_xpath(data)
        elif node_type == "function":
            return self._parse_function(data)
        elif node_type == "expression":
            return self._parse_expression(data)
        else:
            raise ValueError(f"未知节点类型: {node_type}")

    def _parse_xpath(self, data: Dict) -> XPathNode:
        """解析XPath节点"""
        args = data.get("args", [])
        parsed_parts = [self.parse(part) for part in args]
        return XPathNode(parsed_parts, source=data)

    def _parse_function(self, data: Dict) -> FunctionNode:
        """解析函数节点"""
        args = data.get("args", [])

        if not args:
            raise ValueError("函数节点必须至少有一个参数（函数名）")

        # 第一个参数是函数名
        func_name = self._parse_function_name(args[0])

        # 解析函数参数
        parsed_args = [self.parse(arg) for arg in args[1:]]

        return FunctionNode(func_name, parsed_args, source=data)

    def _parse_function_name(self, name_data) -> str:
        """解析函数名，支持字符串或变量引用"""
        if isinstance(name_data, str):
            return name_data
        elif isinstance(name_data, dict) and name_data.get("type") == "variable":
            return name_data["name"]
        else:
            raise ValueError(f"无效的函数名格式: {name_data}")

    def _parse_expression(self, data: Dict) -> ExpressionNode:
        """解析表达式节点"""
        operator = data.get("operator")
        if not operator:
            raise ValueError("表达式节点缺少operator字段")

        args = data.get("args", [])
        parsed_operands = [self.parse(arg) for arg in args]

        return ExpressionNode(operator, parsed_operands, source=data)

    def _parse_list(self, data: list) -> List[ExprASTNode]:
        """解析列表（视为隐式表达式）"""
        # 如果列表中只有一个元素，直接解析该元素
        if len(data) == 1:
            return [self.parse(data[0])]

        # 多个元素视为隐式连接表达式
        return [self.parse(item) for item in data]


class ExprASTVisitor(ABC):
    """访问者模式基类"""

    @abstractmethod
    def visit_xpath(self, node: XPathNode):
        pass

    @abstractmethod
    def visit_function(self, node: FunctionNode):
        pass

    @abstractmethod
    def visit_expression(self, node: ExpressionNode):
        pass

    @abstractmethod
    def visit_literal(self, node: LiteralNode):
        pass


class ExprPrintVistor(ExprASTVisitor):
    """打印ExprAST节点的访问者"""

    def visit_xpath(self, node: XPathNode) -> str:
        return "/".join(part.accept(self) for part in node.parts)

    def visit_function(self, node: FunctionNode) -> str:
        # 1. Visit param
        args_str = ", ".join(arg.accept(self) for arg in node.args)
        
        # 2. Try to exec function if registerd
        if function_registry.functions.get(node.name):
            try:
                result = node.execute(node.source)
                return str(result)
            except Exception as e:
                return f"<ERROR: {str(e)}>"
            
        return f"{node.name}({args_str})"

    def visit_expression(self, node: ExpressionNode) -> str:
        # 处理特殊运算符
        if node.operator == "concat":
            return "".join(op.accept(self) for op in node.operands)

        # 处理二元运算符
        if len(node.operands) >= 2:
            left = self._maybe_parenthesize(node.operands[0])
            right = self._maybe_parenthesize(node.operands[1])
            return f"{left} {node.operator} {right}"

        # 处理一元运算符
        if len(node.operands) == 1:
            operand = self._maybe_parenthesize(node.operands[0])
            return f"{node.operator} {operand}"

        # 默认处理：用操作符连接所有操作数
        return f" {node.operator} ".join(op.accept(self) for op in node.operands)

    def _maybe_parenthesize(self, node: ExprASTNode) -> str:
        """根据需要为子表达式添加括号"""
        result = node.accept(self)
        if isinstance(node, ExpressionNode):
            return f"({result})"
        return result

    def visit_literal(self, node: LiteralNode) -> str:
        # 根据类型决定是否添加引号
        return str(node.value)


class ExprValidater(ExprASTVisitor):
    """节点有效性检查器"""

    def __init__(self):
        self.errors = []

    def visit_xpath(self, node: XPathNode) -> bool:
        is_valid: bool = True
        for part in node.parts:
            if part.accept(self) is False:
                is_valid = False
                break
        return is_valid

    def visit_function(self, node: FunctionNode) -> bool:
        # 这里可以添加特定函数的类型检查规则
        for arg in node.args:
            arg.accept(self)

        # 示例：检查node:value函数参数数量
        if node.name == "node:value" and len(node.args) != 1:
            self.errors.append(f"函数 {node.name} 需要1个参数，但得到 {len(node.args)}")

        return True

    def visit_expression(self, node: ExpressionNode):
        # 检查操作数类型是否兼容
        operand_types = [op.accept(self) for op in node.operands]

        # 示例：检查比较运算符的操作数类型
        if node.operator in ["=", "!=", "<", ">"]:
            if len(operand_types) != 2:
                self.errors.append(f"比较运算符 '{node.operator}' 需要2个操作数")
            elif operand_types[0] != operand_types[1]:
                self.errors.append(
                    f"类型不匹配: {operand_types[0]} 和 {operand_types[1]}"
                )

    def visit_literal(self, node: LiteralNode) -> str:
        return node.data_type
