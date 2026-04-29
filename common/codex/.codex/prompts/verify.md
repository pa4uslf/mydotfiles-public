# verify

> 本文件是本地工程编排里的“完成前总闸门”。
>
> 它与 `quality-gate.md` 的区别：
>
> - `quality-gate`：迭代中频繁跑，范围小
> - `verify`：交付前跑，范围全

## 目标

在宣布完成、准备提交、准备评审或准备发布前，对当前代码状态做一轮完整、分层、有结论的验证。

不要把 `verify` 当成一串机械命令；它的目标是回答：

- 这次改动真的可交付吗
- 哪些风险还没被覆盖
- 还差什么证据

## 模式

`$ARGUMENTS` 可取：

- `quick`
  - 快速判断当前分支是否还在健康轨道上
- `full`
  - 默认；完整验证
- `pre-commit`
  - 面向提交前
- `pre-pr`
  - 面向评审/合并前，必要时附加更严格检查

## 执行顺序

### 0. 识别项目命令

先识别项目实际使用的：

- build
- typecheck
- lint
- unit / integration / e2e test
- coverage

不要凭空假设命令名。

### 1. Build

- 跑构建或最接近真实打包/编译的命令
- 如果 build 失败，直接判定 `FAIL`

### 2. Type / Static Analysis

- 跑类型检查
- 跑静态分析
- 收集 file:line 级别错误

### 3. Lint / Format Health

- 跑 lint
- 如项目有 formatter check，也纳入结果
- 区分 warning 和 blocking issue

### 4. Tests

至少区分：

- unit
- integration
- e2e

按改动性质决定是否都必须覆盖：

- 纯库逻辑：unit 至少通过
- 接口/数据流：integration 必须覆盖
- 用户流程/UI/浏览器行为：E2E 必须考虑

如果项目本身没有某一层测试，要明确写成“缺口”，不要假装已验证。

### 5. Diff-aware Checks

对照本次改动，再补以下检查：

- 是否有新增 public API 未测
- 是否有迁移/配置变化未验证
- 是否有 docs drift
- 是否有 console/debug 残留
- 是否有明显 secrets / token / key 泄漏

### 6. Git State

输出：

- 当前未提交改动
- 当前验证面向的是哪些文件/范围

### 7. Readiness Decision

最后必须给出明确结论：

- `READY`
- `READY WITH RISKS`
- `NOT READY`

## 输出格式

默认输出：

```text
VERIFICATION: PASS | FAIL

Mode:      quick | full | pre-commit | pre-pr
Scope:     [files / package / repo]
Build:     OK | FAIL
Types:     OK | X errors
Lint:      OK | X issues
Unit:      X/Y passed | not run | missing
Integration: X/Y passed | not run | missing
E2E:       X/Y passed | not run | missing
Docs:      OK | drift found | not applicable
Secrets:   OK | X findings
Logs:      OK | X findings

Ready:     YES | NO | WITH RISKS
```

如果失败或有风险，优先列：

1. 阻断问题
2. 仍未覆盖的风险
3. 下一步建议

## 结果判定

### PASS

仅当以下条件同时满足时：

- 关键命令通过
- 关键测试层通过或明确不适用
- 无明显阻断问题
- 主要行为已有证据

### FAIL

满足任一项即可：

- build/type/lint/test 有阻断失败
- 高风险改动缺关键验证
- 存在明显 secrets / debug residue / config drift
- 关键信息不足，无法判断是否可交付

### READY WITH RISKS

适用于：

- 核心验证通过
- 但仍有非阻断缺口
- 这些缺口必须被明确写出

## 与其他节点的关系

- 实现阶段的局部反馈用 `quality-gate.md`
- 调试问题先走 `debug.md`
- 高风险改动完成后再补 `code-review.md`
