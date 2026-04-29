# update-docs

> 本文件是本地工程编排里的“文档同步节点”。
>
> 它的目标不是写漂亮文案，而是让文档继续和真实 source of truth 一致。

## 什么时候使用

优先用于：

- 代码改完后需要同步 README / CONTRIBUTING / RUNBOOK / API docs
- 更新命令、环境变量、流程、验证方式
- 变更了工程规则、质量闸门、工作流入口
- 发布前/发布后做文档对账

## 核心原则

1. source of truth 优先
   - 从代码、配置、脚本、schema、spec、工作流文档生成或更新说明
2. 不在错误的位置修文档
   - dotfiles 管理的文件改 dotfiles 源文件，不改家目录副本
3. 文档只补真实变化
   - 不为了“看起来完整”瞎扩写
4. 先找 drift，再改内容

## 先识别 source of truth

常见来源：

| Source of truth | 常见目标文档 |
| --- | --- |
| `package.json` / `Makefile` / `Cargo.toml` / `pyproject.toml` | 命令参考、开发指南 |
| `.env.example` / sample config | 环境变量文档 |
| `openapi.yaml` / route files / handlers | API 文档 |
| `README` 中明确引用的脚本与入口 | 使用说明 |
| `AGENTS.md` / `ENGINEERING.md` / `AGENT_SPEC.md` / prompts | 工程工作流文档 |
| `Dockerfile` / deploy config / CI config | 部署与运维说明 |

## 默认流程

### 1. 找 drift

先问：

- 这次代码改动改变了什么对外事实
- 哪些文档现在已经不准确
- 哪些文档只是可优化，但并未过时

只优先修“已经错误”的文档。

### 2. 找正确编辑位置

如果文档受 dotfiles 管理：

- 修改 dotfiles 源文件
- 不直接在 `~/.codex` 或家目录副本上改

如果文档属于项目仓库：

- 在项目源文件改

### 3. 更新最小必要范围

优先更新：

- 命令说明
- 验证流程
- 环境变量
- API / contract
- 发布/回滚/运行手册
- 工程工作流入口

### 4. 检查生成与手写边界

如果文档存在“可生成区域”：

- 只更新生成区
- 保留手写区

如果没有明确分区：

- 做最小、可审查的人工更新

### 5. 做一致性回看

确认以下内容相互一致：

- `AGENTS.md`
- `ENGINEERING.md`
- `AGENT_SPEC.md`
- 相关 prompts
- README / CONTRIBUTING / RUNBOOK / API 文档

## 当前环境特别规则

针对本地 Codex 环境，若本次变更涉及工程编排或入口规则，优先检查：

- `~/.codex/AGENTS.md`
- `~/.codex/ENGINEERING.md`
- `~/.codex/AGENT_SPEC.md`
- `~/.codex/prompts/*.md`

若这些文件由 dotfiles 管理，则对应修改：

- `~/.dotfiles/common/codex/.codex/...`

## 输出要求

说明：

- 更新了哪些文档
- 每份文档对应的 source of truth 是什么
- 哪些文档被刻意跳过，为什么
- 是否还有潜在 drift 未处理

## 不要做的事

- 不要为没变化的东西重写文档
- 不要在家目录副本和 dotfiles 源文件之间来回打补丁
- 不要创建一堆没有维护计划的新文档
- 不要把猜测写成事实
