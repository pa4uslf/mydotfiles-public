# quality-gate

> 本文件是本地工程编排里的“迭代中局部闸门”。
>
> 它服务于开发中途的快速反馈，不替代 `verify.md`。

## 使用场景

在以下时机优先跑 quality gate：

- 刚改完一个切片
- 重构后想确认没有把当前范围搞坏
- 提交前先做 scoped 自检
- 想快速发现 lint/type/test 问题，而不是等到最后一起处理

## 参数

`$ARGUMENTS`:

- `[path|.]`
  - 默认当前目录
- `--fix`
  - 在工具支持时允许自动修复
- `--strict`
  - 尽量把 warning 也当失败处理

## 原则

- 范围小
- 反馈快
- 紧贴当前修改
- 有问题立刻修，不攒到最后

## 执行流程

### 1. 确定目标范围

优先聚焦：

- 当前修改文件
- 当前 package / module
- 当前用户流相关目录

### 2. 检测工具链

识别该范围对应的：

- formatter
- linter
- type checker
- 目标测试命令

### 3. 执行局部检查

优先顺序：

1. format / lint
2. type
3. targeted tests
4. 必要时 scoped build

### 4. 生成修复清单

输出应简洁说明：

- 哪些检查通过
- 哪些失败
- 最先该修什么

## 与 verify 的关系

### quality-gate 负责

- 开发过程中的高频反馈
- 范围受限的质量检查
- 尽早暴露问题

### verify 负责

- 完成前的全局交付判断
- 全仓或完整影响面的验证
- Ready / Not Ready 结论

简化理解：

- `quality-gate` = iteration gate
- `verify` = release gate

## 输出模板

```text
QUALITY GATE: PASS | FAIL

Scope:    [path/module]
Format:   OK | FAIL
Lint:     OK | FAIL
Types:    OK | FAIL
Tests:    OK | FAIL | not run

Next:
- highest priority fix
- optional follow-up checks
```

## 何时升级为 verify

满足任一条件就从 quality gate 升级到 `verify.md`：

- 功能已经完成
- 准备提交/评审
- 当前改动跨模块
- 涉及用户流、接口、迁移或高风险路径
