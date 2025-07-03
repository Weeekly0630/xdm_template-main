from typing import (
    Optional,
    List,
    Dict,
    Any,
    TypeVar,
    Iterable,
    Union,
    Protocol,
    Callable,
)

""" 
    1. 函数注册表，代表有哪些函数可以使用 
    2. 函数实现类，一个可以实现函数注册表的子类
"""


class FunctionRegistry:
    """函数注册表，用于管理自定义函数"""

    def __init__(self):
        self.functions = {}

    def register(self, name: str, func: Callable, description: str = ""):
        """
        注册自定义函数

        :param name: 函数名
        :param func: 可调用函数
        :param description: 函数描述
        """
        self.functions[name] = {"func": func, "description": description}

    def get(self, name: str) -> Callable:
        """获取注册的函数"""
        if name not in self.functions:
            raise KeyError(f"函数 '{name}' 未注册")
        return self.functions[name]["func"]

    def list_functions(self) -> dict:
        """列出所有注册的函数"""
        return {name: info["description"] for name, info in self.functions.items()}


# 创建全局函数注册表
function_registry = FunctionRegistry()


# 函数接口定义
def custom_function(*args, context: Optional[dict] = None) -> Any:
    """
    自定义函数接口

    :param args: 函数参数
    :param context: 执行上下文（可选）
    :return: 函数执行结果
    """
    # 实际函数实现会覆盖此定义
    pass
