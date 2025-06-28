# ECU Functions Guide in AUTOSAR XPath

本指南详细介绍了AUTOSAR XPath中的ECU相关函数的使用方法。

## 目录
- [ecu:get](#ecuget)
- [ecu:has](#ecuhas)
- [ecu:list](#eculist)
- [最佳实践](#best-practices)
- [常见使用场景](#common-scenarios)

## ecu:get
### 描述
获取ECU配置值，用于访问ECU的配置参数、特性和设置。

### 语法
```xpath
ecu:get('配置路径')
```

### 参数
- `配置路径`: String - ECU配置的完整路径，使用点号分隔层级

### 返回值
- String - 配置的值
- 常见返回值类型：
  * 'STD_ON'/'STD_OFF' - 功能开关状态
  * 'TRUE'/'FALSE' - 布尔值
  * 数值字符串 - 如 '65535'
  * 配置字符串 - 如 'FULL', 'BASIC'

### 使用示例

1. 检查功能是否启用：
```xpath
<a:tst expr="ecu:get('Can.CanConfigSet.CanFdEnable')='STD_ON'" />
```

2. 获取硬件特性：
```xpath
<a:tst expr="ecu:get('AdcDMAPresent')='TRUE'" />
```

3. 条件配置：
```xpath
<a:tst expr="(ecu:get('McuClockFrequency') >= 80) and (.='HighSpeed')" />
```

## ecu:has
### 描述
检查ECU是否具有特定的功能或能力。

### 语法
```xpath
ecu:has('特性名称')
```

### 参数
- `特性名称`: String - 要检查的功能或特性的标识符

### 返回值
- Boolean - true表示ECU具有该特性，false表示不具有

### 使用示例

1. 检查特定功能支持：
```xpath
<a:tst expr="ecu:has('CanFD')" />
```

2. 条件验证：
```xpath
<a:tst expr="not(ecu:has('BasicOnly') and .='ADVANCED')" />
```

3. 组合检查：
```xpath
<a:tst expr="ecu:has('DMA') and ecu:has('HighSpeedCAN')" />
```

## ecu:list
### 描述
获取ECU配置值的列表，可用于枚举可用的配置选项。

### 语法
```xpath
ecu:list('前缀')
```

### 参数
- `前缀`: String (可选) - 用于筛选配置项的前缀

### 返回值
- Array - 符合条件的配置键列表

### 使用示例

1. 获取所有CAN相关配置：
```xpath
<a:tst expr="count(ecu:list('Can.')) > 0" />
```

2. 检查特定配置组是否存在：
```xpath
<a:tst expr="count(ecu:list('Adc.AdcConfigSet.')) >= 1" />
```

3. 遍历配置：
```xpath
<a:foreach items="ecu:list('Can.CanController.')" var="ctrl">
    <a:tst expr="node:value($ctrl) != ''" />
</a:foreach>
```

## Best Practices
### 1. 错误处理
```xpath
<!-- 使用node:fallback处理可能不存在的配置 -->
<a:tst expr="node:fallback(ecu:get('OptionalFeature'), 'STD_OFF') = 'STD_ON'" />
```

### 2. 配置路径规范
```xpath
<!-- 使用完整的配置路径 -->
ecu:get('ModuleName.ConfigSet.Parameter')  // 好
ecu:get('Parameter')                       // 避免
```

### 3. 条件组合
```xpath
<!-- 合理组织多个条件 -->
<a:tst expr="(ecu:has('AdvancedFeature') and 
             ecu:get('Module.Feature') = 'STD_ON') or
             ecu:get('Alternative.Feature') = 'STD_ON'" />
```

### 4. 性能优化
```xpath
<!-- 缓存频繁使用的值 -->
<a:var name="clockFreq" value="ecu:get('McuClockFrequency')" />
<a:tst expr="$clockFreq >= 80 and $clockFreq <= 100" />
```

## Common Scenarios

### 1. 功能可见性控制
```xpath
<a:a name="VISIBLE" type="XPath">
    <a:tst expr="ecu:get('Can.CanConfig.Feature')='STD_ON'" />
</a:a>
```

### 2. 值范围验证
```xpath
<a:tst expr="(. >= ecu:get('MinValue')) and (. <= ecu:get('MaxValue'))" />
```

### 3. 特性依赖检查
```xpath
<a:tst expr="not((.='ADVANCED') and ecu:get('BasicVersionOnly')='TRUE')" />
```

### 4. 硬件兼容性检查
```xpath
<a:tst expr="(ecu:has('HighEndMcu') and .='PERFORMANCE') or
             (not(ecu:has('HighEndMcu')) and .='BASIC')" />
```

### 5. 配置有效性验证
```xpath
<!-- 检查DMA配置 -->
<a:tst expr="(ecu:get('DmaChannelsCount') > 0) and
             (. <= ecu:get('MaxDmaChannels'))" />
```

### 6. 默认值处理
```xpath
<a:def value="ecu:get('Module.DefaultValue')" />
<a:tst expr=". = node:fallback(ecu:get('Module.AllowedValue'), '0')" />
```

### 7. 交叉验证
```xpath
<!-- 验证相关配置的一致性 -->
<a:tst expr="(ecu:get('Feature1')='STD_ON') = (ecu:get('Feature2')='STD_ON')" />
```

### 8. 动态范围检查
```xpath
<a:tst expr="num:i(.) <= num:i(ecu:get('MaximumValue'))" />
```

## 故障排除与提示

### 1. 配置路径问题
- 确保配置路径准确无误
- 注意大小写，配置路径通常是大小写敏感的
- 使用ecu:list()验证路径是否存在

### 2. 类型转换
- ecu:get()返回的始终是字符串
- 需要数值比较时使用num:i()进行转换
- 布尔值比较时注意'TRUE'/'FALSE'是字符串

### 3. 常见错误
- 路径不存在返回空字符串
- 未使用node:fallback导致空值错误
- 配置路径层级错误

### 4. 调试技巧
- 使用ecu:list()查看可用配置
- 验证配置值是否符合预期
- 检查配置路径的层级结构

## 总结
ECU函数提供了强大的配置访问和验证能力：
- ecu:get() 用于获取配置值
- ecu:has() 用于检查功能特性
- ecu:list() 用于枚举配置选项

合理使用这些函数可以：
- 实现动态配置验证
- 控制功能可见性
- 确保配置一致性
- 提供更好的用户体验
