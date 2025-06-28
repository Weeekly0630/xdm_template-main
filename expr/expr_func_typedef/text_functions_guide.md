# Text Functions Guide in AUTOSAR XPath

本指南详细介绍了AUTOSAR XPath中的文本处理相关函数的使用方法。

## 目录
- [基本文本操作](#基本文本操作)
  * [text:contains](#textcontains)
  * [text:toupper](#texttoupper)
  * [text:split](#textsplit)
  * [text:join](#textjoin)
- [文本匹配和替换](#文本匹配和替换)
  * [text:match](#textmatch)
  * [text:grep](#textgrep)
  * [text:replaceAll](#textreplaceall)
- [比较和验证](#比较和验证)
  * [text:difference](#textdifference)
  * [text:uniq](#textuniq)
- [最佳实践](#最佳实践)
- [常见使用场景](#常见使用场景)

## 基本文本操作

### text:contains
#### 描述
检查文本是否包含指定的子字符串。

#### 语法
```xpath
text:contains(haystack, needle)
```

#### 参数
- `haystack`: String - 要搜索的文本
- `needle`: String - 要查找的子字符串

#### 返回值
- Boolean - true表示包含，false表示不包含

#### 使用示例
```xpath
<!-- 基本文本搜索 -->
<a:tst expr="text:contains('HelloWorld', 'World')" />

<!-- 配置值检查 -->
<a:tst expr="text:contains(node:value(Description), 'CONFIG')" />
```

### text:toupper
#### 描述
将文本转换为大写。

#### 语法
```xpath
text:toupper(text)
```

#### 参数
- `text`: String - 要转换的文本

#### 返回值
- String - 转换后的大写文本

#### 使用示例
```xpath
<!-- 基本转换 -->
<a:tst expr="text:toupper('hello') = 'HELLO'" />

<!-- 配置值标准化 -->
<a:tst expr="text:toupper(Status) = 'ENABLED'" />
```

### text:split
#### 描述
将文本按指定的分隔符分割成数组。

#### 语法
```xpath
text:split(text, delimiter)
```

#### 参数
- `text`: String - 要分割的文本
- `delimiter`: String - 分隔符

#### 返回值
- Array - 分割后的字符串数组

#### 使用示例
```xpath
<!-- 基本分割 -->
<a:tst expr="text:split('a,b,c', ',')[2] = 'b'" />

<!-- 配置值解析 -->
<a:tst expr="text:split(Parameters, ';')[1] = 'Value'" />
```

### text:join
#### 描述
将数组元素用指定的分隔符连接成字符串。

#### 语法
```xpath
text:join(array, delimiter)
```

#### 参数
- `array`: Array - 要连接的数组
- `delimiter`: String - 分隔符

#### 返回值
- String - 连接后的字符串

#### 使用示例
```xpath
<!-- 基本连接 -->
<a:tst expr="text:join(('a', 'b', 'c'), ',') = 'a,b,c'" />

<!-- 配置值组合 -->
<a:tst expr="text:join(Parameters/*/Value, ';')" />
```

## 文本匹配和替换

### text:match
#### 描述
使用正则表达式匹配文本。

#### 语法
```xpath
text:match(text, pattern[, flags])
```

#### 参数
- `text`: String - 要匹配的文本
- `pattern`: String - 正则表达式模式
- `flags`: String (可选) - 正则表达式标志

#### 返回值
- Boolean - true表示匹配成功，false表示匹配失败

#### 使用示例
```xpath
<!-- 基本正则匹配 -->
<a:tst expr="text:match(Name, '^[a-zA-Z_][a-zA-Z0-9_]*$')" />

<!-- 配置值验证 -->
<a:tst expr="text:match(Version, '^\d+\.\d+\.\d+$')" />
```

### text:grep
#### 描述
在文本中搜索匹配正则表达式的部分。

#### 语法
```xpath
text:grep(text, pattern)
```

#### 参数
- `text`: String - 要搜索的文本
- `pattern`: String - 正则表达式模式

#### 返回值
- Array - 匹配的文本数组

#### 使用示例
```xpath
<!-- 提取数字 -->
<a:tst expr="count(text:grep(Content, '\d+')) > 0" />

<!-- 查找标识符 -->
<a:tst expr="text:grep(Code, '[A-Z]+_\d+')" />
```

### text:replaceAll
#### 描述
替换文本中所有匹配模式的部分。

#### 语法
```xpath
text:replaceAll(text, pattern, replacement)
```

#### 参数
- `text`: String - 原始文本
- `pattern`: String - 要替换的模式
- `replacement`: String - 替换文本

#### 返回值
- String - 替换后的文本

#### 使用示例
```xpath
<!-- 基本替换 -->
<a:tst expr="text:replaceAll('a-b-c', '-', '_') = 'a_b_c'" />

<!-- 格式化路径 -->
<a:tst expr="text:replaceAll(Path, '\\', '/') = 'path/to/file'" />
```

## 比较和验证

### text:difference
#### 描述
比较两个文本的差异。

#### 语法
```xpath
text:difference(text1, text2)
```

#### 参数
- `text1`: String - 第一个文本
- `text2`: String - 第二个文本

#### 返回值
- String - 差异描述

#### 使用示例
```xpath
<!-- 配置比较 -->
<a:tst expr="text:difference(OldConfig, NewConfig) = ''" />

<!-- 版本比较 -->
<a:tst expr="text:difference(Version, RequiredVersion)" />
```

### text:uniq
#### 描述
检查文本在给定上下文中是否唯一。

#### 语法
```xpath
text:uniq(value, context)
```

#### 参数
- `value`: String - 要检查的值
- `context`: NodeSet - 检查上下文

#### 返回值
- Boolean - true表示唯一，false表示不唯一

#### 使用示例
```xpath
<!-- 名称唯一性检查 -->
<a:tst expr="text:uniq(Name, ../*/Name)" />

<!-- ID唯一性验证 -->
<a:tst expr="text:uniq(ID, //*/ID)" />
```

## 最佳实践

### 1. 文本比较
```xpath
<!-- 规范化后比较 -->
<a:tst expr="text:toupper(Value1) = text:toupper(Value2)" />
```

### 2. 正则表达式使用
```xpath
<!-- 使用合适的模式 -->
<a:tst expr="text:match(Identifier, '^[A-Za-z][A-Za-z0-9_]*$')" />
```

### 3. 分割与连接
```xpath
<!-- 安全的分割与连接 -->
<a:tst expr="text:join(text:split(Value, ','), ';')" />
```

### 4. 唯一性验证
```xpath
<!-- 多层次唯一性检查 -->
<a:tst expr="text:uniq(ID, //Module/*/ID) and text:uniq(Name, ../*/Name)" />
```

## 常见使用场景

### 1. 名称验证
```xpath
<!-- 标识符格式检查 -->
<a:tst expr="text:match(Name, '^[A-Z][a-zA-Z0-9]*$')" />
```

### 2. 路径处理
```xpath
<!-- 路径规范化 -->
<a:tst expr="text:replaceAll(FilePath, '\\\\', '/')" />
```

### 3. 配置解析
```xpath
<!-- 参数提取 -->
<a:tst expr="text:split(Configuration, ';')[1] = 'ENABLED'" />
```

### 4. 版本比较
```xpath
<!-- 版本号验证 -->
<a:tst expr="text:match(Version, '^\d+\.\d+\.\d+$')" />
```

## 注意事项与技巧

### 1. 字符串处理
- 注意大小写敏感性
- 使用适当的转义
- 考虑空白字符的影响

### 2. 正则表达式
- 使用合适的模式
- 注意性能影响
- 处理特殊字符

### 3. 文本比较
- 规范化后比较
- 考虑字符编码
- 处理边界情况

### 4. 性能优化
- 避免过度使用正则表达式
- 适当缓存结果
- 选择合适的函数

## 总结
文本函数提供了强大的文本处理能力：
- 全面的文本操作功能
- 灵活的模式匹配
- 可靠的文本验证

合理使用这些函数可以：
- 提高文本处理效率
- 确保数据格式正确
- 简化复杂的文本操作
- 增强配置的可靠性
