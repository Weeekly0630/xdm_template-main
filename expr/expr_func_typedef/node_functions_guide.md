# Node Functions Guide in AUTOSAR XPath

本指南详细介绍了AUTOSAR XPath中的Node相关函数的使用方法。

## 目录
- [基础函数](#基础函数)
  * [node:value](#nodevalue)
  * [node:exists](#nodeexists)
  * [node:current](#nodecurrent)
- [引用操作](#引用操作)
  * [node:ref](#noderef)
  * [node:refs](#noderefs)
  * [node:refexists](#noderefexists)
  * [node:refvalid](#noderefvalid)
- [节点内容检查](#节点内容检查)
  * [node:contains](#nodecontains)
  * [node:containsValue](#nodecontainsvalue)
  * [node:empty](#nodeempty)
- [节点属性](#节点属性)
  * [node:name](#nodename)
  * [node:paths](#nodepaths)
- [条件和过滤](#条件和过滤)
  * [node:filter](#nodefilter)
  * [node:when](#nodewhen)
  * [node:islast](#nodeislast)
- [错误处理](#错误处理)
  * [node:fallback](#nodefallback)
- [最佳实践](#最佳实践)
- [常见使用场景](#常见使用场景)

## 基础函数

### node:value
#### 描述
获取节点的值。

#### 语法
```xpath
node:value(node)
```

#### 参数
- `node`: Node (可选) - 要获取值的节点。如果省略，默认为当前节点(.)

#### 返回值
- String - 节点的值

#### 使用示例
```xpath
<!-- 获取当前节点值 -->
<a:tst expr="node:value(.) = 'ExpectedValue'" />

<!-- 获取其他节点值 -->
<a:tst expr="node:value(../Parameter) = 'ValidValue'" />
```

### node:exists
#### 描述
检查节点是否存在。

#### 语法
```xpath
node:exists(path)
```

#### 参数
- `path`: String - 要检查的节点路径

#### 返回值
- Boolean - true表示节点存在，false表示不存在

#### 使用示例
```xpath
<!-- 检查配置节点是否存在 -->
<a:tst expr="node:exists(CanControllerRef)" />

<!-- 检查可选特性是否存在 -->
<a:tst expr="node:exists(../OptionalFeature)" />
```

### node:current
#### 描述
返回当前上下文节点。

#### 语法
```xpath
node:current()
```

#### 参数
无

#### 返回值
- Node - 当前上下文节点

#### 使用示例
```xpath
<!-- 计算子节点数量 -->
<a:tst expr="count(node:current()/*) > 0" />

<!-- 检查当前节点类型 -->
<a:tst expr="name(node:current()) = 'Configuration'" />
```

## 引用操作

### node:ref
#### 描述
获取单个引用节点。

#### 语法
```xpath
node:ref(path)
```

#### 参数
- `path`: String - 引用节点的路径

#### 返回值
- Node - 被引用的节点

#### 使用示例
```xpath
<!-- 获取控制器配置 -->
<a:tst expr="node:ref('ASPathDataOfSchema:/TS_T40D2M10I1R0/Can/CanController')" />

<!-- 检查引用节点的值 -->
<a:tst expr="node:value(node:ref(ControllerRef)) = 'Active'" />
```

### node:refs
#### 描述
获取多个引用节点。

#### 语法
```xpath
node:refs(path)
```

#### 参数
- `path`: String - 引用节点的路径

#### 返回值
- NodeSet - 被引用节点的集合

#### 使用示例
```xpath
<!-- 检查所有通道配置 -->
<a:tst expr="count(node:refs('ASPathDataOfSchema:/DmaChannels')/*) > 0" />

<!-- 验证所有引用的状态 -->
<a:tst expr="count(node:refs(AllControllers)/State[.='Active']) > 0" />
```

### node:refexists
#### 描述
检查引用是否存在。

#### 语法
```xpath
node:refexists(reference)
```

#### 参数
- `reference`: Node - 要检查的引用节点

#### 返回值
- Boolean - true表示引用存在，false表示不存在

#### 使用示例
```xpath
<!-- 检查控制器引用是否存在 -->
<a:tst expr="node:refexists(CanControllerRef)" />

<!-- 条件验证 -->
<a:tst expr="not(node:refexists(OptionalRef)) or node:value(OptionalRef) = 'Valid'" />
```

### node:refvalid
#### 描述
验证引用是否有效。

#### 语法
```xpath
node:refvalid(reference)
```

#### 参数
- `reference`: Node - 要验证的引用节点

#### 返回值
- Boolean - true表示引用有效，false表示无效

#### 使用示例
```xpath
<!-- 验证必需引用 -->
<a:tst expr="node:refvalid(ControllerRef)" />

<!-- 条件验证 -->
<a:tst expr="node:refvalid(.) or node:value(../AllowEmpty)='true'" />
```

## 节点内容检查

### node:contains
#### 描述
检查节点是否包含特定值。

#### 语法
```xpath
node:contains(node, value)
```

#### 参数
- `node`: Node - 要检查的节点
- `value`: String - 要查找的值

#### 返回值
- Boolean - true表示包含，false表示不包含

#### 使用示例
```xpath
<!-- 检查配置值 -->
<a:tst expr="node:contains(SupportedFeatures, 'DMA')" />

<!-- 验证列表内容 -->
<a:tst expr="node:contains(AllowedValues, node:value(.))" />
```

### node:containsValue
#### 描述
检查节点值是否包含特定字符串。

#### 语法
```xpath
node:containsValue(node, searchString)
```

#### 参数
- `node`: Node - 要检查的节点
- `searchString`: String - 要查找的字符串

#### 返回值
- Boolean - true表示包含，false表示不包含

#### 使用示例
```xpath
<!-- 检查描述文本 -->
<a:tst expr="node:containsValue(Description, 'Configuration')" />

<!-- 验证命名规则 -->
<a:tst expr="node:containsValue(Name, 'Prefix_')" />
```

### node:empty
#### 描述
检查节点是否为空。

#### 语法
```xpath
node:empty(node)
```

#### 参数
- `node`: Node - 要检查的节点

#### 返回值
- Boolean - true表示节点为空，false表示不为空

#### 使用示例
```xpath
<!-- 检查必填字段 -->
<a:tst expr="not(node:empty(.))" />

<!-- 条件检查 -->
<a:tst expr="node:empty(OptionalConfig) or node:value(OptionalConfig) = 'Valid'" />
```

## 节点属性

### node:name
#### 描述
获取节点的名称。

#### 语法
```xpath
node:name(node)
```

#### 参数
- `node`: Node - 要获取名称的节点

#### 返回值
- String - 节点的名称

#### 使用示例
```xpath
<!-- 检查节点类型 -->
<a:tst expr="node:name(.) = 'Configuration'" />

<!-- 验证父节点 -->
<a:tst expr="node:name(..) = 'Container'" />
```

### node:paths
#### 描述
获取节点的完整路径。

#### 语法
```xpath
node:paths(node)
```

#### 参数
- `node`: Node - 要获取路径的节点

#### 返回值
- String - 节点的完整路径

#### 使用示例
```xpath
<!-- 检查节点位置 -->
<a:tst expr="node:paths(.) = '/Configuration/Parameters'" />

<!-- 验证引用路径 -->
<a:tst expr="node:paths(node:ref(Reference)) = ExpectedPath" />
```

## 条件和过滤

### node:filter
#### 描述
根据条件过滤节点集。

#### 语法
```xpath
node:filter(nodes, condition)
```

#### 参数
- `nodes`: NodeSet - 要过滤的节点集
- `condition`: String - 过滤条件

#### 返回值
- NodeSet - 符合条件的节点集

#### 使用示例
```xpath
<!-- 过滤活动配置 -->
<a:tst expr="count(node:filter(*/Configuration, 'State=Active')) > 0" />

<!-- 选择有效节点 -->
<a:tst expr="count(node:filter(., 'Value!=null')) = 1" />
```

### node:when
#### 描述
基于条件返回不同的值。

#### 语法
```xpath
node:when(condition, trueValue, falseValue)
```

#### 参数
- `condition`: Boolean - 判断条件
- `trueValue`: Any - 条件为true时返回的值
- `falseValue`: Any - 条件为false时返回的值

#### 返回值
- Any - 根据条件返回相应的值

#### 使用示例
```xpath
<!-- 条件值设置 -->
<a:tst expr="node:when(node:exists(Feature), 'Enabled', 'Disabled')" />

<!-- 配置选择 -->
<a:tst expr="node:when(count(*)>0, 'Valid', 'Empty')" />
```

### node:islast
#### 描述
检查是否是最后一个节点。

#### 语法
```xpath
node:islast(node)
```

#### 参数
- `node`: Node - 要检查的节点

#### 返回值
- Boolean - true表示是最后一个节点，false表示不是

#### 使用示例
```xpath
<!-- 检查序列位置 -->
<a:tst expr="node:islast(.)" />

<!-- 条件处理 -->
<a:tst expr="not(node:islast(.)) or FinalFlag='true'" />
```

## 错误处理

### node:fallback
#### 描述
提供默认值处理机制。

#### 语法
```xpath
node:fallback(primaryValue, fallbackValue)
```

#### 参数
- `primaryValue`: Any - 首选值
- `fallbackValue`: Any - 当首选值不可用时的替代值

#### 返回值
- Any - primaryValue存在时返回primaryValue，否则返回fallbackValue

#### 使用示例
```xpath
<!-- 安全的值访问 -->
<a:tst expr="node:fallback(OptionalParameter, 'default') = 'Valid'" />

<!-- 配置回退 -->
<a:tst expr="node:value(node:fallback(../Config, DefaultConfig)) = 'Active'" />
```

## 最佳实践

### 1. 安全的值访问
```xpath
<!-- 使用node:fallback避免空值错误 -->
<a:tst expr="node:fallback(node:value(OptionalNode), 'default') = 'ExpectedValue'" />
```

### 2. 引用验证
```xpath
<!-- 验证引用完整性 -->
<a:tst expr="node:refexists(.) and node:refvalid(.)" />
```

### 3. 条件处理
```xpath
<!-- 使用node:when进行优雅的条件处理 -->
<a:tst expr="node:when(node:exists(Feature), 
                      node:value(Feature),
                      'DefaultValue')" />
```

### 4. 路径验证
```xpath
<!-- 使用node:paths进行位置验证 -->
<a:tst expr="contains(node:paths(.), '/Expected/Path')" />
```

## 常见使用场景

### 1. 配置验证
```xpath
<!-- 验证必需配置 -->
<a:tst expr="node:exists(Required) and not(node:empty(Required))" />
```

### 2. 引用完整性
```xpath
<!-- 检查引用链完整性 -->
<a:tst expr="node:refvalid(ControllerRef) and 
             node:refvalid(node:ref(ControllerRef)/SubRef)" />
```

### 3. 条件配置
```xpath
<!-- 基于条件的配置检查 -->
<a:tst expr="node:when(node:exists(../Advanced),
                      'AdvancedMode',
                      'BasicMode')" />
```

### 4. 值范围验证
```xpath
<!-- 使用node:value进行范围检查 -->
<a:tst expr="num:i(node:value(.)) >= 0 and 
             num:i(node:value(.)) <= 100" />
```

### 5. 模块依赖检查
```xpath
<!-- 验证模块依赖关系 -->
<a:tst expr="not(node:exists(../RequiredModule)) or
             node:refvalid(../RequiredModule)" />
```

## 注意事项与技巧

### 1. 空值处理
- 使用node:fallback处理可能的空值
- 在访问可选节点前检查node:exists
- 使用node:empty验证必需值

### 2. 引用链处理
- 验证每个引用节点的有效性
- 使用node:refexists预检查
- 合理使用node:ref和node:refs

### 3. 路径处理
- 使用node:paths验证节点位置
- 注意路径的相对和绝对表示
- 验证关键路径点

### 4. 性能优化
- 避免重复的节点访问
- 合理使用node:filter减少遍历
- 缓存频繁使用的值

## 总结
Node函数提供了强大的节点操作和验证能力：
- 安全的值访问和错误处理
- 完整的引用管理机制
- 灵活的条件处理
- 强大的节点过滤和验证

合理使用这些函数可以：
- 提高配置的可靠性
- 简化复杂的验证逻辑
- 提供更好的错误处理
- 实现高效的节点操作
