# HARNESS.md

这份文档定义“harness engineering 项目”在 Codex 环境中的默认创建约束。

目标不是生成一个“看起来很全”的空仓库，而是先把 agent 能稳定执行的工程 harness 搭好，再开始堆业务代码。

## 1. 核心原则

### 1.1 先搭 harness，再写功能

最先落地的应该是：

1. 项目目标和非目标
2. 执行计划
3. 架构边界
4. 统一验证入口
5. agent 导航入口

如果这些东西不存在，先补它们，不要直接进入实现。

### 1.2 仓库是 system of record

需求、计划、约束、验证脚本必须留在仓库里，而不是只存在一次性 prompt 中。

原则：

- `AGENTS.md` 负责短入口
- 详细规则沉淀到 `README.md`、`ARCHITECTURE.md`、`WORKFLOW.md`、`docs/`、`scripts/`
- agent 应该主要通过读仓库获得上下文，而不是依赖会话记忆

### 1.3 对 agent 可读，比对人类“显得聪明”更重要

优先：

- 短文件入口
- 清楚的目录分工
- 明确的 done criteria
- 可机械执行的脚本

避免：

- 超长 `AGENTS.md`
- 只有自然语言、没有脚本化验证
- 文档和代码互相漂移

### 1.4 约束必须能被机械检查

凡是重要的边界，尽量都要有脚本对应：

- 架构边界 -> `scripts/check-architecture.*`
- 质量闸门 -> `scripts/verify.*`
- 安全扫描 -> `scripts/security-scan.*`
- API / schema 同步 -> 对应脚本或测试

只靠“记得遵守”通常会失效。

## 2. 什么时候适合用 harness engineering

下面这些场景优先用：

1. 需求会持续迭代，不是一次性脚本
2. 计划让 agent 长期参与开发
3. 需要把 issue -> 实现 -> 验证 -> review 变成稳定流程
4. 需要并行处理多个任务
5. 需要把质量、安全、架构边界提前固化

如果只是十分钟内的一次性实验脚本，不必强行上完整 harness。

## 3. 新项目的最低交付骨架

创建 harness engineering 项目时，默认至少准备这些文件：

```text
.
├── .gitignore
├── README.md
├── AGENTS.md
├── .agentlens/INDEX.md
├── ARCHITECTURE.md
├── WORKFLOW.md
├── docs/
│   ├── product-spec.md
│   ├── reference/
│   │   └── api.md          # 仅在有 API / 协议时需要
│   ├── exec-plans/
│   │   └── initial-delivery.md
│   └── security-audit.md   # 可先作为基线/模板
├── scripts/
│   ├── check-architecture.*
│   ├── verify.*
│   └── security-scan.*     # 有发布/安全要求时
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
```

说明：

- `AGENTS.md` 必须短，只做导航和硬约束入口
- 如果 `AGENTS.md` 提到了 `.agentlens/INDEX.md`，这个文件必须真实存在
- 有 HTTP / API 时，再补 `docs/reference/api.md`
- 有发布前检查、安全边界、外部输入面时，再补安全审计与扫描脚本

## 4. 推荐创建顺序

### 4.1 第一步：先补基础仓库卫生

初始化仓库时先做这些：

1. 建立 `.gitignore`
2. 明确运行时版本和包管理器
3. 约定统一验证命令名称，例如 `npm run verify`
4. 约定统一安全扫描命令名称，例如 `npm run scan:security`

`.gitignore` 至少覆盖：

- 日志
- 缓存
- 临时文件
- 本地环境目录
- 系统生成文件
- 测试产物

### 4.2 第二步：文档先行

先写：

1. `README.md`
2. `ARCHITECTURE.md`
3. `docs/product-spec.md`
4. `docs/exec-plans/initial-delivery.md`
5. `WORKFLOW.md`

这些文档未成形前，不要让 agent 大规模进入实现。

### 4.3 第三步：脚本化质量闸门

至少补这些能力：

1. 一个统一 `verify` 入口
2. 单元测试
3. 集成测试
4. E2E 测试
5. 架构边界检查

如果是面向真实输入或准备发布：

1. 依赖审计
2. secrets 扫描
3. 静态安全扫描
4. Git 历史 secrets 检查

### 4.4 第四步：最后才是业务实现

只有当前三步完成后，才进入业务代码。

## 5. 各关键文件应该承担什么责任

### 5.1 `AGENTS.md`

只保留最短入口和硬规则，例如：

- 开工前先读哪些文件
- 修改后必须跑什么命令
- 哪些变更要同步更新哪些文档
- 哪些类型任务要触发额外扫描

不要把完整产品 spec、详细架构、长篇 workflow 都堆在这里。

### 5.2 `.agentlens/INDEX.md`

提供仓库导航索引，帮助 agent 快速找到：

- 关键文档
- 核心目录
- 常用脚本
- 测试入口
- 最近重点改动区域

如果项目要求“开始前先读 `.agentlens/INDEX.md`”，就必须把它维护为真实可用的入口，不能悬空。

### 5.3 `README.md`

负责回答：

1. 这是什么项目
2. 如何启动
3. 如何验证
4. 仓库怎么导航
5. 这个仓库如何体现 harness engineering

### 5.4 `ARCHITECTURE.md`

负责定义：

1. 分层职责
2. 允许依赖方向
3. 禁止跨层导入
4. 质量闸门

重要约束：

> 任何层级变化，都必须同时更新 `ARCHITECTURE.md` 和架构检查脚本。

### 5.5 `docs/product-spec.md`

至少包含：

1. Goal
2. Inputs / Outputs
3. Non-goals
4. Acceptance Criteria

没有清楚的验收标准，就不算可以并行执行的任务。

### 5.6 `docs/exec-plans/*.md`

执行计划按 change / issue 拆分，至少包含：

1. Goal
2. Scope
3. Risks
4. Tasks
5. Exit Criteria

原则：

- 一项真实工作至少对应一个执行计划
- 先更新计划，再改代码
- 完成后要把计划收敛到当前事实

### 5.7 `WORKFLOW.md`

这是给 `openai/symphony` 或其他编排器看的仓库级流程文件。

至少写清：

1. Objective
2. Required Inputs
3. Execution Rules
4. Done Criteria
5. Review Focus

没有 `WORKFLOW.md`，多 agent 编排通常会退化成“谁先动手谁算”。

## 6. Symphony 集成约束

结合 `openai/symphony` 的公开设计，默认遵守这些约束：

1. 工作单元优先按 issue 管理，不要按“随手一段 prompt”管理
2. 每个 issue 使用独立 workspace / worktree，避免多个 worker 共享脏工作区
3. 并发数按 review 与集成能力控制，不按机器 CPU 上限硬拉满
4. 共享规则必须落在仓库根部可读文件中，例如 `AGENTS.md`、`WORKFLOW.md`、`docs/`
5. 结果必须能通过 reviewer / 汇总节点核对，而不是只看 worker 自述
6. 对外部系统的状态回写必须基于明确 done criteria，不靠主观判断

补充约束：

- 若任务会改同一批文件，不要盲目并行
- 若需求还没澄清，不要急着交给编排器大规模启动 worker
- 若 `verify` 还没成型，不要把项目伪装成“可自动化交付”

## 7. 默认质量闸门

任何成熟 harness 项目都应尽量具备一个统一入口，例如：

```bash
npm run verify
```

这个入口应至少覆盖：

1. 架构边界检查
2. 单元测试
3. 集成测试
4. E2E 测试

以下命令建议独立保留：

```bash
npm run audit:deps
npm run scan:security
```

触发条件：

- 依赖变化 -> 跑 `audit:deps`
- 发布前检查、安全相关改动、输入边界变化、认证授权变化、API 改动 -> 跑 `scan:security`

## 8. 默认安全基线

如果项目是服务、API、SaaS、Agent 平台或任何处理外部输入的系统，创建时就默认考虑：

1. 输入边界与 schema 校验
2. 请求体大小限制
3. `Content-Type` 校验
4. 认证与授权
5. 速率限制
6. 结构化日志
7. secrets 检查
8. 依赖漏洞审计
9. 静态安全扫描
10. 公开机器可读接口说明，例如 `openapi.json`

如果环境受限，安全扫描允许有离线降级路径，但必须把降级事实写进 `docs/security-audit.md`。

## 9. 推荐目录分层

如果是后端或全栈业务项目，默认优先考虑清晰分层，例如：

- `src/domain`: 纯业务规则
- `src/application`: 用例编排和边界校验
- `src/infrastructure`: HTTP / DB / queue / adapter
- `src/shared`: 跨层基础工具
- `tests`: 与层次对应的 unit / integration / e2e

这不是唯一答案，但必须满足：

1. 依赖方向单向
2. 业务规则可脱离适配层独立测试
3. 基础设施代码不反向污染领域规则

## 10. 创建时常见反模式

下面这些情况，默认判定 harness 还没搭好：

1. `AGENTS.md` 巨长，且和 `docs/` 大量重复
2. `AGENTS.md` 指向不存在的文件
3. 只有 README，没有产品 spec / 执行计划 / workflow
4. 有测试目录，但没有统一 `verify` 入口
5. 有架构分层口号，但没有架构检查脚本
6. 需求、计划、验证都只存在聊天记录里
7. 多个 worker 在同一工作区并行乱改
8. 完成标准写成“差不多可以了”
9. 安全扫描完全依赖发布前人工想起来再做
10. 文档最后补，导致 agent 总是按旧上下文工作

## 11. 一个可复用的创建检查表

创建 harness engineering 项目时，默认检查：

- `.gitignore` 已补齐常见忽略项
- `README.md` 已写清启动、验证、导航
- `AGENTS.md` 是短入口，不是大杂烩
- `.agentlens/INDEX.md` 真实存在且可读
- `ARCHITECTURE.md` 已定义层级和导入边界
- `docs/product-spec.md` 已定义验收标准
- `docs/exec-plans/initial-delivery.md` 已存在
- `WORKFLOW.md` 已定义执行和完成规则
- `scripts/verify.*` 已存在并可运行
- `tests/unit`、`tests/integration`、`tests/e2e` 已建好
- 安全和依赖扫描入口已明确
- 若要接 Symphony，issue/workspace/review 流程已能闭环

全部满足后，才算“可以让 agent 稳定参与开发”。

## 12. 参考来源

这些规则主要来自三类输入的收敛：

1. OpenAI《Harness Engineering》文章中的原则：短 `AGENTS.md`、结构化仓库上下文、可验证的 harness、agent 可读性优先
2. `openai/symphony` 公开仓库中对 `WORKFLOW.md`、issue 驱动、workspace 隔离、多 worker 协作与 review 汇总的要求
3. 当前 `19harness_engineering_demo` 项目里已经验证有效的做法：文档先行、`verify` 统一闸门、架构检查脚本、安全扫描入口、分层目录和执行计划
