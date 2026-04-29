# tdd

> 本文件是本地工程编排里的“实现节点”。
>
> 它吸收的是 superpowers 风格的核心纪律，而不是机械照搬所有步骤：
>
> - bug 先复现
> - feature 先定义行为
> - 先红后绿
> - 最小实现
> - 绿后再重构
> - 以验证证据结束，而不是以“代码写完”结束

## 前置条件

进入本节点前，应该已经明确：

- 目标
- 约束
- 边界
- 验收方式

这些信息通常来自：

- `ENGINEERING.md`
- `plan.md`
- 对于高风险任务，来自 `AGENT_SPEC.md`

## 何时使用

默认用于：

- 新功能实现
- bug 修复
- 行为敏感的重构
- 核心业务逻辑修改

## 默认节奏

### 1. 定义行为边界

先明确：

- 输入输出
- 关键状态转换
- 错误路径
- 不应改变的外部行为

如果是 bug：

- 先用测试、最小复现脚本、日志断言或快照证明当前行为错误

如果是 feature：

- 先定义成功行为和关键边界条件

### 2. RED

先制造失败证据，再写实现。

优先级：

1. 单元测试
2. 集成测试
3. E2E 测试
4. 最小可复现实验

要求：

- 失败原因必须正确
- 测试名要说明具体行为
- 至少覆盖 happy path 和关键 edge/error path

### 3. GREEN

只写让当前失败证据变绿所需的最小代码。

要求：

- 不顺手扩 scope
- 不趁机大规模抽象
- 不在尚未被测试要求的地方提前优化

### 4. REFACTOR

在测试全绿的前提下再做：

- 命名修正
- 结构整理
- 重复消除
- 抽象提炼
- 注释补充

如果 refactor 让范围变大：

- 先停下来
- 重新回到 `plan.md`

### 5. 局部质量闸门

每完成一个有意义的切片，就跑一次局部检查：

- formatter / lint / type
- 相关测试
- 必要时 scoped build

这一步走 `quality-gate.md`，不要等到最后一起爆炸。

### 6. 总验证

实现完成后，不在本节点里宣布结束。

必须进入：

- `verify.md`
- 高风险改动再补 `code-review.md`

## Bug Fix 特化规则

修 bug 时默认顺序：

1. 复现
2. 缩小范围
3. 根因假设
4. 写失败证据
5. 最小修复
6. 补回归测试
7. 验证无副作用

禁止：

- 没有根因线索就直接改实现
- 只凭肉眼看代码猜测“应该是这里”
- 修完不补回归证据

## Feature 特化规则

做 feature 时默认顺序：

1. 从用户行为切片开始
2. 先实现最小可交付路径
3. 每个切片都带验证
4. 最后再补扩展能力

优先：

- 垂直切片
- 可运行、可验证的小步前进

避免：

- 先铺一整层底座却没有用户价值证明
- 先写一堆抽象和配置再落功能

## 常见实现顺序

### 后端

1. contract / schema / interface
2. failing tests
3. service / handler / persistence 最小实现
4. error handling
5. refactor
6. verify

### 前端

1. states / props / user flows
2. failing tests or interaction checks
3. minimal UI and state wiring
4. edge states / loading / empty / error
5. polish only after behavior green
6. verify / E2E

### 跨前后端

1. 先固定对外 contract
2. 后端与前端各自做最小可验证切片
3. 用集成/E2E 串起来
4. 最后处理性能、观感和次要路径

## 完成定义

离开本节点前，至少满足：

- 当前切片的失败证据已经变绿
- 新增行为有测试或其他可重复证据
- 回归点已覆盖
- 没有明显 scope creep 未记录
- 已准备进入 `verify.md`
