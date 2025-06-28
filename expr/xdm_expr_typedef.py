from dataclasses import dataclass
from typing import Optional, Union, List, Dict, Any
from enum import Enum, auto

class XdmElementType(Enum):
    """定义XDM元素的类型。"""
    STRING = auto()    # 简单字符串值
    XPATH = auto()     # XPath表达式
    FUNCTION = auto()  # 函数调用
    EXPRESSION = auto() # 复合表达式

class XdmElement:
    """XDM元素的基类，所有XDM元素都继承自此类。"""
    def __init__(self, value: Union[str, List[Any]], element_type: Optional[XdmElementType] = None):
        self.value = value
        self.type = element_type or XdmElementType.STRING

    def __str__(self) -> str:
        if isinstance(self.value, str):
            return self.value
        elif isinstance(self.value, list):
            return "".join(str(x) for x in self.value)
        return str(self.value)

@dataclass
class XdmFunctionInfo:
    """Holds information about a function in the XDM function library."""
    name: str
    min_params: int       # 最小参数个数
    max_params: int       # 最大参数个数，-1表示无限
    description: Optional[str] = None
    handler_name: Optional[str] = None  # 可选的处理函数
    
    @property
    def param_count(self) -> int:
        """兼容旧代码，返回最小参数个数"""
        return self.min_params

@dataclass
class XdmOperatorInfo:
    """存储操作符的相关信息。"""
    display: str           # 显示字符串，如 ">", "&&" 等
    min_params: int       # 最小参数个数
    max_params: int       # 最大参数个数，-1表示无限
    description: Optional[str] = None  # 操作符描述

class XdmOperator(Enum):
    """Defines available XDM operators."""
    NONE = 0
    EQUAL = 1
    NOT_EQUAL = 2
    LESS_THAN = 3
    LESS_THAN_OR_EQUAL = 4
    GREATER_THAN = 5
    GREATER_THAN_OR_EQUAL = 6
    AND = 7
    OR = 8
    NOT = 9

    @property
    def info(self) -> XdmOperatorInfo:
        """Returns the operator information."""
        _OPERATOR_INFO = {
            XdmOperator.NONE: XdmOperatorInfo("", 0, 0),
            XdmOperator.EQUAL: XdmOperatorInfo("=", 2, 2, "相等比较"),
            XdmOperator.NOT_EQUAL: XdmOperatorInfo("!=", 2, 2, "不相等比较"),
            XdmOperator.LESS_THAN: XdmOperatorInfo("&lt;", 2, 2, "小于比较"),
            XdmOperator.LESS_THAN_OR_EQUAL: XdmOperatorInfo("&lt;=", 2, 2, "小于等于比较"),
            XdmOperator.GREATER_THAN: XdmOperatorInfo("&gt;", 2, 2, "大于比较"),
            XdmOperator.GREATER_THAN_OR_EQUAL: XdmOperatorInfo("&gt;=", 2, 2, "大于等于比较"),
            XdmOperator.AND: XdmOperatorInfo("and", 2, -1, "逻辑与运算"),
            XdmOperator.OR: XdmOperatorInfo("or", 2, -1, "逻辑或运算"),
            XdmOperator.NOT: XdmOperatorInfo("not", 1, 1, "逻辑非运算"),
        }
        return _OPERATOR_INFO[self]

    def __str__(self) -> str:
        """Returns the string representation of the operator."""
        return self.info.display

class XdmFunctionLibrary:
    """Library containing XDM function definitions and metadata."""
    
    def __init__(self):
        """初始化函数库"""
        self._functions = {}
        self.current_node = None
        self.root_node = None
        self.initialize_functions()
    
    def set_root_node(self, root_node: Any):
        """设置根节点（通常只需要设置一次）"""
        self.root_node = root_node
        
    def set_current_node(self, node: Any):
        """设置当前处理的节点"""
        self.current_node = node
    
    def initialize_functions(self):
        """初始化所有函数定义"""
        self._functions = {
        # user defined functions
        "user:get_rel_xpath": XdmFunctionInfo(
            name="user:get_rel_xpath",
            min_params=1,
            max_params=2,
            description="Get relative XPath expression between nodes. Args: target_path, [source_path]",
            handler_name="handle_user_function"
        ),
        
        # node functions
        "node:exists": XdmFunctionInfo(
            name="node:exists",
            min_params=1,
            max_params=1,
            description="Check if a node exists"
        ),
        "node:value": XdmFunctionInfo(
            name="node:value",
            min_params=1,
            max_params=1,
            description="Get value of a node"
        ),
        "node:current": XdmFunctionInfo(
            name="node:current",
            min_params=0,
            max_params=0,
            description="Reference current node"
        ),
        "node:ref": XdmFunctionInfo(
            name="node:ref",
            min_params=1,
            max_params=1,
            description="Get referenced node"
        ),
        "node:refvalid": XdmFunctionInfo(
            name="node:refvalid",
            min_params=1,
            max_params=1,
            description="Check if reference is valid"
        ),
        "node:fallback": XdmFunctionInfo(
            name="node:fallback",
            min_params=1,
            max_params=2,
            description="Provide fallback value, second argument is optional default value"
        ),
        "node:contains": XdmFunctionInfo(
            name="node:contains",
            min_params=1,
            max_params=2,
            description="Check if node contains value, with optional pattern"
        ),

        # text functions
        "text:match": XdmFunctionInfo(
            name="text:match",
            min_params=2,
            max_params=3,
            description="Pattern matching with optional flags"
        ),
        "text:contains": XdmFunctionInfo(
            name="text:contains",
            min_params=2,
            max_params=2,
            description="String contains"
        ),
        "text:split": XdmFunctionInfo(
            name="text:split",
            min_params=1,
            max_params=2,
            description="Split string with optional separator"
        ),
        "text:uniq": XdmFunctionInfo(
            name="text:uniq",
            min_params=1,
            max_params=1,
            description="Check uniqueness"
        ),

        # numeric functions
        "num:i": XdmFunctionInfo(
            name="num:i",
            min_params=1,
            max_params=2,
            description="Convert to integer with optional base"
        ),
        "count": XdmFunctionInfo(
            name="count",
            min_params=1,
            max_params=1,
            description="Count elements"
        ),

        # ecu functions
        "ecu:get": XdmFunctionInfo(
            name="ecu:get",
            min_params=1,
            max_params=2,
            description="Get ECU configuration value with optional default"
        ),
        "ecu:has": XdmFunctionInfo(
            name="ecu:has",
            min_params=1,
            max_params=1,
            description="Check if ECU has capability"
        ),
        "ecu:list": XdmFunctionInfo(
            name="ecu:list",
            min_params=0,
            max_params=1,
            description="Get list of ECU values with optional pattern"
        ),
        
        }

    def get_function_info(self, func_name: str) -> Optional[XdmFunctionInfo]:
        """Gets function information for a given function name."""
        return self._functions.get(func_name)

    def handle_user_function(self, func_name: str, args: List[str]) -> str:
        """处理用户自定义函数"""
        if func_name == "user:get_rel_xpath":
            if not self.current_node:
                raise ValueError("No current node set for path calculation")
                
            if len(args) not in [1, 2]:
                raise ValueError("get_rel_xpath requires 1 or 2 arguments")
                
            # 获取目标节点路径
            target_yaml_path = args[0]
            
            # 获取源节点路径（可选）
            source_yaml_path = args[1] if len(args) > 1 else None
            
            # 将相对路径转换为绝对路径（相对于当前节点的yaml文件目录）
            from pathlib import Path
            current_dir = Path(self.current_node.info).parent
            
            if not self.root_node:
                raise ValueError("Root node not set")
                
            from .. import get_project_root
            
            # 获取项目根目录（通过全局设置）
            try:
                root_dir = get_project_root()
            except RuntimeError:
                # 如果没有设置全局根目录，则使用root_node的父目录
                root_dir = Path(self.root_node.info).parent.resolve()
            
            # 打印调试信息
            print(f"Debug Info:")
            print(f"  Current node: {self.current_node.info}")
            print(f"  Project root: {root_dir}")
            print(f"  Current dir: {current_dir}")
            
            def resolve_path(path: str) -> str:
                try:
                    if path.startswith('/'):  # 绝对路径（相对于项目根目录）
                        # 去掉开头的/，然后从项目根目录解析
                        clean_path = path.lstrip('/')
                        # 从项目根目录解析绝对路径
                        resolved_path = str((root_dir / clean_path).resolve())
                        print(f"  Resolving absolute path: '{path}' -> '{resolved_path}'")
                        return resolved_path
                    else:  # 相对路径（相对于当前YAML文件目录）
                        # 从当前文件目录解析相对路径
                        resolved_path = str((current_dir / path).resolve())
                        print(f"  Resolving relative path: '{path}' -> '{resolved_path}'")
                        return resolved_path
                except Exception as e:
                    raise ValueError(f"Failed to resolve path '{path}': {str(e)}")
            
            # 查找目标节点
            target_abs_path = resolve_path(target_yaml_path)
            target_node = self.current_node.find_by_yaml_path(target_abs_path)
            if not target_node:
                raise ValueError(f"Target node not found: {target_yaml_path}")
            
            # 获取源节点
            source_node = self.current_node
            if source_yaml_path:
                source_abs_path = resolve_path(source_yaml_path)
                source_node = self.current_node.find_by_yaml_path(source_abs_path)
                if not source_node:
                    raise ValueError(f"Source node not found: {source_yaml_path}")
            
            # 计算相对路径
            return source_node.get_relative_xpath_to(target_node)
                
        raise ValueError(f"Unknown user function: {func_name}")
        
    def register_function(
        self, 
        name: str, 
        min_params: int, 
        max_params: Optional[int] = None, 
        description: Optional[str] = None
    ):
        """注册一个新的函数到库中。

        Args:
            name: 函数名
            min_params: 最小参数个数
            max_params: 最大参数个数，如果为None则等于min_params
            description: 函数描述
        """
        self._functions[name] = XdmFunctionInfo(
            name=name,
            min_params=min_params,
            max_params=max_params if max_params is not None else min_params,
            description=description
        )

    def get_function_help(self, func_name: Optional[str] = None) -> str:
        """获取函数的帮助信息。

        Args:
            func_name: 函数名，如果不指定则返回所有函数的信息

        Returns:
            函数的帮助信息字符串
        """
        if func_name is not None:
            func_info = self.get_function_info(func_name)
            if not func_info:
                return f"Unknown function: {func_name}"
            params = (
                f"{func_info.min_params}"
                if func_info.min_params == func_info.max_params
                else f"{func_info.min_params}-{func_info.max_params}"
            )
            return f"{func_info.name}  [params: {params}]\n  {func_info.description}"

        # 返回所有函数的信息，按类型分组
        result = []
        funcs_by_type = {}
        for fname, finfo in self._functions.items():
            ftype = fname.split(":")[0] if ":" in fname else "other"
            if ftype not in funcs_by_type:
                funcs_by_type[ftype] = []
            funcs_by_type[ftype].append(finfo)

        for ftype, finfos in sorted(funcs_by_type.items()):
            result.append(f"\n{ftype.upper()} Functions:")
            for finfo in sorted(finfos, key=lambda x: x.name):
                params = (
                    f"{finfo.min_params}"
                    if finfo.min_params == finfo.max_params
                    else f"{finfo.min_params}-{finfo.max_params}"
                )
                result.append(f"  {finfo.name}  [params: {params}]")
                if finfo.description:
                    result.append(f"    {finfo.description}")

        return "\n".join(result)
    
    def process_function(self, func_name: str, args: List[str]) -> Optional[str]:
        """
        处理函数调用。

        Args:
            func_name: 函数名
            args: 函数参数

        Returns:
            函数处理结果
        """
        func_info = self.get_function_info(func_name)
        if not func_info or not func_info.handler_name:
            raise ValueError(f"Function '{func_name}' is not defined or has no handler")
        
        handler = getattr(self, func_info.handler_name, None)
        if not handler:
            raise ValueError(f"No handler found for function '{func_name}'")
        
        return handler(args)
        
    def handle_get_relative_xpath(self, args: List[str]) -> str:
        """
        获取从一个节点到另一个节点的相对XPath表达式。

        Args:
            args[0]: 起始节点路径
            args[1]: 目标节点路径

        Returns:
            str: 相对XPath表达式
        """
        if not self.current_node:
            raise ValueError("No current node context available")

        if len(args) != 2:
            raise ValueError("get_rel_xpath requires exactly 2 arguments")

        # 从当前节点查找源节点和目标节点
        from_node = self.current_node.find_by_absolute_path(args[0])
        if not from_node:
            raise ValueError(f"Source node not found: {args[0]}")

        to_node = self.current_node.find_by_absolute_path(args[1])
        if not to_node:
            raise ValueError(f"Target node not found: {args[1]}")

        # 计算相对路径
        return from_node.get_relative_xpath_to(to_node)

class XdmXPathValue(XdmElement):
    """表示一个XPath表达式值。参数形式为: xpath arg1 arg2 ..."""
    def __init__(self, args: List[Union[str, XdmElement]]):
        super().__init__(args, XdmElementType.XPATH)
    
    def __str__(self) -> str:
        """返回XPath表达式。
        将参数列表用'/'连接，并用括号包围整个XPath表达式以提高可读性。
        """
        xpath = '/'.join(str(arg) for arg in self.value)
        return f"({xpath})"

class XdmFunctionValue(XdmElement):
    """表示一个函数调用。第一个参数为函数名，后面的参数为函数参数。"""
    def __init__(self, args: List[Union[str, XdmElement]], func_lib: XdmFunctionLibrary):
        super().__init__(args, XdmElementType.FUNCTION)
        if not args:
            raise ValueError("Function must have a name as first argument")
        
        self.func_lib = func_lib  # 保存函数库引用
        
        # 获取函数名并验证函数是否存在
        func_name = str(args[0])
        func_info = func_lib.get_function_info(func_name)
        if not func_info:
            supported_functions = ", ".join(f"'{func}'" for func in func_lib._functions.keys())
            raise ValueError(
                f"Unknown function: '{func_name}'. "
                f"Supported functions are: [{supported_functions}]"
            )
            
        # 验证参数个数
        actual_params = len(args) - 1  # 减去函数名参数
        if actual_params < func_info.min_params:
            raise ValueError(
                f"Function '{func_name}' expects at least {func_info.min_params} parameter(s), but got {actual_params}"
            )
        if func_info.max_params != -1 and actual_params > func_info.max_params:
            raise ValueError(
                f"Function '{func_name}' expects at most {func_info.max_params} parameter(s), but got {actual_params}"
            )

    def __str__(self) -> str:
        """返回函数调用表达式。"""
        args = [str(arg) for arg in self.value]
        func_name = args[0]
        func_args = args[1:]
        
        # 处理用户自定义函数
        if func_name.startswith("user:"):
            try:
                return self.func_lib.handle_user_function(func_name, func_args)
            except Exception as e:
                # 如果处理失败，返回原始函数调用格式并提供错误信息
                print(f"Warning: Failed to handle user function: {e}")
        
        # 返回标准函数调用格式
        return f"{func_name}({', '.join(func_args)})"

class XdmExpression(XdmElement):
    """表示一个XDM表达式。第一个参数是操作符，后面的参数根据操作符定义确定。"""
    def __init__(self, args: List[Union[XdmOperator, XdmElement]]):
        if not args:
            raise ValueError("Expression must have an operator as first argument")
        
        if not isinstance(args[0], XdmOperator):
            raise ValueError("First argument must be an operator")
            
        operator = args[0]
        operands = args[1:]
        
        # 验证参数个数
        op_info = operator.info
        if op_info.max_params != -1 and len(operands) > op_info.max_params:
            raise ValueError(
                f"Operator '{operator}' expects maximum {op_info.max_params} parameter(s), but got {len(operands)}"
            )
        if len(operands) < op_info.min_params:
            raise ValueError(
                f"Operator '{operator}' expects minimum {op_info.min_params} parameter(s), but got {len(operands)}"
            )
            
        self.type = XdmElementType.EXPRESSION
        super().__init__(args, self.type)

    def __str__(self) -> str:
        """返回表达式的字符串表示。"""
        operator = self.value[0]
        operands = self.value[1:]
        
        if operator == XdmOperator.NOT:
            # 一元操作符特殊处理
            return f"({operator} {str(operands[0])})"
            
        # 二元或多元操作符
        op_str = f" {operator} "
        return f"({op_str.join(str(op) for op in operands)})"
