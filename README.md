<p align="center">
  <img src="https://raw.githubusercontent.com/kt-aicoding/.github/main/assets/logo.svg" alt="KT AI Coding logo" width="96" />
</p>

# KT AI Coding Skills

面向 AI 编程 Agent 的可复用技能集合，用来沉淀组织级判断、工作流、检查清单和客户端特定操作规范。

这个仓库不放应用 demo，也不放泛 prompt。每个 skill 应该让 Agent 在一个可重复任务上做出更稳定的判断或执行更可靠的流程。

## 目录规划

```text
skills/
  codex/
  claude-code/
  shared/
```

| 路径 | 用途 |
| --- | --- |
| `skills/codex/` | Codex skills，包含 `SKILL.md`、`agents/` 和可选 references |
| `skills/claude-code/` | Claude Code 专用技能或命令规范 |
| `skills/shared/` | 跨客户端通用的 Agent 工作流资料 |

## 当前 Skills

| Skill | 路径 | 用途 |
| --- | --- | --- |
| CLI Tooling Governance | `skills/codex/cli-tooling-governance` | 判断 CLI、脚本、MCP、skill、独立仓库之间的边界，治理 CLI 工具成熟度和升级策略 |
| Goal Prompt Builder | `skills/codex/goal-prompt-builder` | 将复杂请求整理成长时间可续跑、可验证、可审计收口的 goal 提示词 |
| MCP Surface Governance | `skills/codex/mcp-surface-governance` | 判断能力是否适合暴露为 MCP server，设计小而安全的 tool surface |
| KT AI Coding Registry | `skills/codex/kt-aicoding-registry` | 判断 AI coding 资产应归属哪个 kt-aicoding 仓库，并维护 catalog/README 一致性 |

## 设计原则

- 每个 skill 聚焦一个可重复执行的工作流。
- 跨客户端通用的内容优先放到 `shared/`。
- 客户端特有行为放到对应客户端目录。
- 详细判断表放到 `references/`，保持 `SKILL.md` 精简。
- 不提交 token、cookie、API key、私有路径或私有业务上下文。

## 相关仓库

| 仓库 | 关系 |
| --- | --- |
| [`kt-aicoding/registry`](https://github.com/kt-aicoding/registry) | 组织级索引和迁移候选 |
| [`kt-aicoding/cli-tools`](https://github.com/kt-aicoding/cli-tools) | CLI 工具和 CLI 治理资料 |
| [`kt-aicoding/mcp-servers`](https://github.com/kt-aicoding/mcp-servers) | MCP server 和 MCP surface 治理资料 |
| [`kt-aicoding/agent-workflows`](https://github.com/kt-aicoding/agent-workflows) | 多 Agent 工作流模板 |
