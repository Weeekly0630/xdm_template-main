# XPath Expressions in AUTOSAR XML
## Basic Comparison Operators

### Numeric Comparisons
- Greater than: `&gt;=value`
- Less than: `&lt;=value`
- Equal: `=value`
- Not equal: `!=value`

Example:
```xml
<a:tst expr="&gt;=0" />
<a:tst expr="&lt;=255" />
```

### Boolean Operations
- AND: `and`
- OR: `or`
- NOT: `not`

## XPath Functions

### node Functions
- `node:exists()` - Check if a node exists
- `node:value()` - Get value of a node
- `node:current()` - Reference current node
- `node:ref()` - Get referenced node
- `node:refs()` - Get Multi referenced node
- `node:refvalid()` - Check if reference is valid
- `node:fallback()` - Provide fallback value
- `node:contains()` - Check if node contains value

Examples:
```xml
<a:tst expr="node:exists(CanControllerRef)" />
<a:tst expr="node:value(.) = 'true'" />
```

### text Functions
- `text:match()` - Pattern matching
- `text:contains()` - String contains
- `text:split()` - Split string
- `text:uniq()` - Check uniqueness

Example:
```xml
<a:tst expr="text:match(normalize-space(.),'^[_a-zA-Z]+[_0-9a-zA-Z]*$')" />
```

### num Functions
- `num:i()` - Convert to integer
- `count()` - Count elements

Example:
```xml
<a:tst expr="num:i(count(node:current()/*)) &lt;= 255" />
```

### ecu Functions
- `ecu:get()` - Get ECU configuration value
- `ecu:has()` - Check if ECU has capability
- `ecu:list()` - Get list of ECU values

Example:
```xml
<a:tst expr="ecu:get('Can.CanConfigSet.CanFdEnable')='STD_ON'" />
```

## Complex Expressions

### Conditional Expressions
```xml
<a:tst expr="(condition1) and (condition2) or (condition3)" />
```

### Position and Index Operations
```xml
<a:tst expr="position()-1=node:fallback(node:current()/../@index,'0')" />
```

### String Manipulation
```xml
<a:tst expr="substring-after(node:value(.), '/Can/Can/')" />
```

## Advanced Function Documentation

### Node Functions

### node:exists()
**Description**: Checks if a specified node exists in the configuration.

**Parameters**:
- `path`: String (optional) - Path to the node to check. If not provided, checks current node.

**Returns**: Boolean - true if the node exists, false otherwise

**Example**:
```xml
<a:tst expr="node:exists(CanControllerRef)" />
```

### node:value()
**Description**: Retrieves the value of a node.

**Parameters**:
- `node`: Node (optional) - The node to get value from. Defaults to current node (.).

**Returns**: String - The value of the node

**Example**:
```xml
<a:tst expr="node:value(.) = 'true'" />
```

### node:current()
**Description**: References the current context node in the configuration.

**Parameters**: None

**Returns**: Node - The current context node

**Example**:
```xml
<a:tst expr="count(node:current()/*) > 0" />
```

### node:ref()
**Description**: Retrieves a single referenced node based on a specified path.

**Parameters**:
- `path`: String - ASPath to the referenced node

**Returns**: Node - The referenced node

**Example**:
```xml
<a:tst expr="node:ref('ASPathDataOfSchema:/TS_T40D2M10I1R0/Can/CanController')" />
```

### node:refs()
**Description**: Retrieves multiple referenced nodes based on a specified path.

**Parameters**:
- `path`: String - ASPath to the referenced nodes

**Returns**: NodeSet - Collection of referenced nodes

**Example**:
```xml
<a:tst expr="node:refs('ASPathDataOfSchema:/TS_T40D2M10I1R0/Mcl')" />
```

### node:refvalid()
**Description**: Validates if a node reference is valid.

**Parameters**:
- `node`: Node - The node containing the reference to validate

**Returns**: Boolean - true if reference is valid, false otherwise

**Example**:
```xml
<a:tst expr="node:refvalid(CanControllerRef)" />
```

### node:fallback()
**Description**: Provides a fallback value if the primary value is not available.

**Parameters**:
- `primary`: Any - The primary value to try
- `fallback`: Any - The fallback value to use if primary is not available

**Returns**: Any - Either the primary value or fallback value

**Example**:
```xml
<a:tst expr="node:fallback(OptionalParameter, 'default')" />
```

### node:contains()
**Description**: Checks if a node contains a specific value.

**Parameters**:
- `node`: Node - The node to check
- `value`: String - The value to look for

**Returns**: Boolean - true if node contains the value, false otherwise

**Example**:
```xml
<a:tst expr="node:contains(SupportedFeatures, 'DMA')" />
```

### Text Functions

### text:match()
**Description**: Performs pattern matching on a string using regular expressions.

**Parameters**:
- `input`: String - The input string to match against
- `pattern`: String - Regular expression pattern
- `flags`: String (optional) - Regex flags (e.g., 'i' for case-insensitive)

**Returns**: Boolean - true if pattern matches, false otherwise

**Example**:
```xml
<a:tst expr="text:match(normalize-space(.),'^[_a-zA-Z]+[_0-9a-zA-Z]*$')" />
```

### text:contains()
**Description**: Checks if a string contains another string.

**Parameters**:
- `haystack`: String - The string to search in
- `needle`: String - The string to search for

**Returns**: Boolean - true if needle is found in haystack, false otherwise

**Example**:
```xml
<a:tst expr="text:contains(node:value(.), 'CONFIG')" />
```

### text:split()
**Description**: Splits a string into an array based on a delimiter.

**Parameters**:
- `input`: String - The string to split
- `delimiter`: String - The delimiter to split on

**Returns**: Array - Array of substrings

**Example**:
```xml
<a:tst expr="text:split(node:value(.), ',')[1] = 'value'" />
```

### text:uniq()
**Description**: Checks if a value is unique within a specified context.

**Parameters**:
- `value`: String - The value to check for uniqueness
- `context`: NodeSet - The context to check within

**Returns**: Boolean - true if value is unique, false otherwise

**Example**:
```xml
<a:tst expr="text:uniq(ShortName, ../*/ShortName)" />
```

### Numeric Functions

### num:i()
**Description**: Converts a value to an integer.

**Parameters**:
- `value`: String|Number - The value to convert

**Returns**: Number - The integer value

**Example**:
```xml
<a:tst expr="num:i('123') = 123" />
```

### count()
**Description**: Counts the number of nodes in a node-set.

**Parameters**:
- `node-set`: NodeSet - The set of nodes to count

**Returns**: Number - The number of nodes in the set

**Example**:
```xml
<a:tst expr="count(*/ConfigParameter) = 3" />
```

### ECU Functions

### ecu:get()
**Description**: Retrieves configuration values from the ECU configuration.

**Parameters**:
- `key`: String - The configuration key to lookup

**Returns**: String - The configuration value

**Example**:
```xml
<a:tst expr="ecu:get('AdcDMAPresent') = 'TRUE'" />
```

### ecu:has()
**Description**: Checks if the ECU has a specific capability or feature.

**Parameters**:
- `feature`: String - The feature to check for

**Returns**: Boolean - true if the ECU has the feature, false otherwise

**Example**:
```xml
<a:tst expr="ecu:has('CanFD')" />
```

### ecu:list()
**Description**: Retrieves a list of available ECU configuration values.

**Parameters**:
- `prefix`: String (optional) - Filter values by prefix

**Returns**: Array - List of available configuration keys

**Example**:
```xml
<a:tst expr="count(ecu:list('Can.')) > 0" />
```

## Complex Configuration Example

### ADC DMA Configuration Validation
The following example demonstrates a complex validation expression for ADC DMA configuration:

```xml
<a:tst expr="(count(
    node:refs('ASPathDataOfSchema:/TS_T40D2M10I1R0/Mcl')/MclConfigSet/*[1]/DMAChannel/*/MclDMAChannelEnable[.='true']/../DmaSource0[.= 'ADC0_COCO'])=0) and
    (.= 'ADC_DMA') and 
    (../AdcHwUnitId = 'ADC0') and 
    ((ecu:get('AdcDMAPresent') = 'TRUE'))" />
```

This expression validates ADC DMA configuration with multiple conditions:

1. **DMA Channel Validation**:
   ```xml
   count(node:refs('ASPathDataOfSchema:/TS_T40D2M10I1R0/Mcl')/MclConfigSet/*[1]/DMAChannel/*/MclDMAChannelEnable[.='true']/../DmaSource0[.= 'ADC0_COCO'])=0
   ```
   - Uses `node:refs()` to access MCL configuration
   - Checks enabled DMA channels
   - Verifies no channel is using ADC0_COCO as source

2. **ADC Trigger Mode**:
   ```xml
   .= 'ADC_DMA'
   ```
   - Validates current node value is ADC_DMA

3. **ADC Unit Check**:
   ```xml
   ../AdcHwUnitId = 'ADC0'
   ```
   - Confirms configuration is for ADC0 unit

4. **Feature Support**:
   ```xml
   ecu:get('AdcDMAPresent') = 'TRUE'
   ```
   - Verifies ECU supports ADC DMA functionality

This example shows how to combine multiple functions and conditions to create comprehensive configuration validation rules.

## Common Use Cases

### Validation Rules
```xml
<a:da name="INVALID" type="XPath">
    <a:tst expr="node:refvalid(.) or node:value(../CanAllowLoopAsCycle)='true'" />
</a:da>
```

### Visibility Control
```xml
<a:a name="VISIBLE" type="XPath">
    <a:tst expr="ecu:get('Can.CanConfig.Feature')='STD_ON'" />
</a:a>
```

### Editability Control
```xml
<a:da name="EDITABLE" type="XPath">
    <a:tst expr="../ParentParameter = 'true'" />
</a:da>
```

### Range Validation
```xml
<a:da name="RANGE" type="XPath">
    <a:tst expr="&gt;=0" />
    <a:tst expr="&lt;=65535" />
</a:da>
```

## Best Practices

1. Always use proper XML escaping for special characters:
   - `&gt;` for >
   - `&lt;` for <
   - `&amp;` for &
   - `&quot;` for "
   - `&apos;` for '

2. Use node:fallback() for safe value access

3. Combine conditions with proper parentheses for clarity

4. Use normalize-space() for string comparisons to handle whitespace

5. Consider performance - avoid deeply nested expressions

`ecu:get()` 是一个用于获取 ECU 配置值的函数，让我详细介绍它的使用方法：

1. 基本语法：

```xpath
ecu:get('配置路径')
```

2. 常见用法：

a) 检查功能是否启用：

```xpath
ecu:get('Can.CanConfigSet.CanFdEnable') = 'STD_ON'
```

b) 获取硬件特性：

```xpath
ecu:get('AdcDMAPresent') = 'TRUE'
```

c) 获取配置参数：

```xpath
ecu:get('Can.CanConfig.MaxMessageLength')
```

3. 路径格式：

- 使用点号分隔层级：`模块.配置集.参数`
- 例如：`Can.CanConfigSet.CanController`

4. 常见应用场景：

a) 功能可见性控制：

```xpath
<a:a name="VISIBLE" type="XPath">
    <a:tst expr="ecu:get('Can.CanConfig.Feature')='STD_ON'" />
</a:a>
```

b) 条件验证：

```xpath
<a:tst expr="(ecu:get('CanFDAvailable') = 'TRUE') and (.='CANFD')" />
```

c) 默认值设置：

```xpath
<a:def value="ecu:get('Can.CanConfig.DefaultBaudRate')" />
```

5. 注意事项：

- 配置路径必须精确匹配

- 返回值通常是字符串

- 常用的返回值：

  - 'STD_ON'/'STD_OFF' - 功能开关
  - 'TRUE'/'FALSE' - 布尔值
  - 数值 - 如 '65535'
  - 字符串 - 如 'FULL' 或 'BASIC'

6. 组合使用示例：

a) 与条件判断：

```xpath
ecu:get('Can.CanConfig.Feature')='STD_ON' and ecu:get('Can.CanFD.Support')='TRUE'
```

b) 与 node:fallback 配合：

```xpath
node:fallback(ecu:get('Can.DefaultValue'), '0')
```

7. 实际应用举例：

a) 检查外设可用性：

```xpath
<a:tst expr="ecu:get('PeripheralAvailable') = 'TRUE'" />
```

b) 验证配置兼容性：

```xpath
<a:tst expr="(ecu:get('McuClockFrequency') >= 80) and (.='HighSpeed')" />
```

c) 特性依赖检查：

```xpath
<a:tst expr="not((.='ADVANCED') and ecu:get('BasicVersionOnly')='TRUE')" />
```

这个函数在 AUTOSAR 配置中非常重要，因为它允许：

1. 根据 ECU 能力动态调整配置选项
2. 实现配置参数的交叉验证
3. 控制功能的可见性和可用性
4. 提供基于硬件能力的默认值
