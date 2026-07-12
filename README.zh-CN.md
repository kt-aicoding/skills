<p align="center">
  <img src="https://raw.githubusercontent.com/kt-aicoding/.github/main/assets/logo.svg" alt="KT AI Coding logo" width="96" />
</p>

# KT AI Coding Skills

面向 Codex CLI、Codex IDE 和 Codex App 的可复用技能集合，用来沉淀组织级判断、工作流与检查清单。

这个仓库不放应用 demo，也不放泛 prompt。每个 Skill 应该让 Codex 在一个可重复任务上做出更稳定的判断或执行更可靠的流程。

## 目录

```text
skills/
  <skill-name>/
```

| 路径 | 用途 |
| --- | --- |
| `skills/<skill-name>/` | Codex Skills，包含 `SKILL.md`、`agents/` 和可选 `references/` |

## 当前 Skills

| Skill | 路径 | 用途 |
| --- | --- | --- |
| CLI Tooling Governance | `skills/cli-tooling-governance` | 判断 CLI、脚本、MCP、Skill、独立仓库之间的边界，治理 CLI 工具成熟度和升级策略 |
| Implementation Workflow | `skills/implementation-workflow` | 将实施计划、可选子 Agent 执行、验证和安全 Git 收口整合成一个 Codex 原生工作流 |
| MCP Surface Governance | `skills/mcp-surface-governance` | 判断能力是否适合暴露为 MCP server，设计小而安全的 tool surface |
| KT AI Coding Registry | `skills/kt-aicoding-registry` | 判断 AI coding 资产应归属哪个 `kt-aicoding` 仓库，并维护 catalog/README 一致性 |

Goal prompt 已由独立仓库 [`kt-aicoding/skill-goal`](https://github.com/kt-aicoding/skill-goal) 维护，避免两个 Skill 竞争同一触发场景。

`implementation-workflow` 是 `writing-plans`、`subagent-driven-development`、
`executing-plans` 和 `finishing-a-development-branch` 的 Codex 原生合并版本。它保留
三个实施阶段，但不复制 Claude Code 的 `TodoWrite`、强制 worktree、自动 commit 或
每个小任务固定调用三名 Agent 等假设。

## 安装到 Codex

推荐在 Codex 中使用内置安装器：

```text
Use $skill-installer to install all Codex skills from https://github.com/kt-aicoding/skills/tree/main/skills.
```

本地开发时，Codex 的用户级 Skill 目录是 `$HOME/.agents/skills`。可以把需要开发的 Skill 链接进去：

```bash
mkdir -p "$HOME/.agents/skills"
for skill in skills/*; do
  target="$HOME/.agents/skills/$(basename "$skill")"
  test -e "$target" || ln -s "$PWD/$skill" "$target"
done
```

Codex 会自动检测 Skill 变化；若列表未刷新，重启 Codex。本仓库目前按独立 Skills 分发；只有在准备好 marketplace 时才整体插件化，避免未发布 Plugin 改变 Skill 的调用名称。

## 验证

```bash
validator="${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py"
for skill in skills/*; do
  python3 "$validator" "$skill"
done
python3 scripts/audit-codex-skills.py --root skills --strict
git diff --check
```

不带 `--root` 时，`scripts/audit-codex-skills.py` 会读取 `$HOME/.agents/skills`、兼容
目录 `$HOME/.codex/skills` 和 `~/.codex/config.toml`，报告同名冲突、完全重复、失效
链接、非 Codex 原生 frontmatter、过长描述，以及自动触发与仅显式调用的数量。默认只审计当前启用项且不修改文件；
使用 `--verbose` 可展开全部发现，`--json` 可生成机器可读结果，使用 `--strict` 可在
CI 中把问题转成非零退出码。

本机的低频专业 Skill 由 `config/codex-explicit-only-skills.txt` 分类管理。它们不会占用
Codex 初始 Skill 目录预算，但仍可通过 `$skill-name` 调用：

```bash
# 检查当前策略是否与清单一致
python3 scripts/manage-codex-skill-policy.py

# Skill 升级覆盖 agents/openai.yaml 后重新应用
python3 scripts/manage-codex-skill-policy.py --apply

# 恢复清单中 Skill 的默认自动触发行为
python3 scripts/manage-codex-skill-policy.py --restore
```

使用量审计只聚合本机保留会话中的会话级命中次数，不写入 prompt、工具输出、工作目录
或 session ID。运行后会更新 `reports/CODEX_SKILL_USAGE.md`：

```bash
python3 scripts/audit-codex-skill-usage.py
```

它分别统计用户显式 `$skill` 和 Codex 读取 `SKILL.md` 的证据，并标记高频长描述、
高频 explicit-only Skill，以及没有保留使用证据但仍自动注入的候选项。`no-evidence`
仅表示当前保留日志没有证据，不代表从未使用。

## 设计原则

- 每个 Skill 聚焦一个可重复执行的工作流。
- `description` 前置关键用途和触发词，避免大量 Skills 安装时被截断后失去辨识度。
- 用户级安装使用 `$HOME/.agents/skills`；仓库级 Skill 使用 `.agents/skills`。
- 详细判断表放到 `references/`，保持 `SKILL.md` 精简。
- 不提交 token、cookie、API key、私有路径或私有业务上下文。

## 相关仓库

| 仓库 | 关系 |
| --- | --- |
| [`kt-aicoding/registry`](https://github.com/kt-aicoding/registry) | 组织级索引和迁移候选 |
| [`kt-aicoding/cli-tools`](https://github.com/kt-aicoding/cli-tools) | CLI 工具和 CLI 治理资料 |
| [`kt-aicoding/mcp-servers`](https://github.com/kt-aicoding/mcp-servers) | MCP server 和 MCP surface 治理资料 |
| [`kt-aicoding/agent-workflows`](https://github.com/kt-aicoding/agent-workflows) | 多 Agent 工作流模板 |
| [`kt-aicoding/skill-goal`](https://github.com/kt-aicoding/skill-goal) | 长时间、可续跑的 Codex goal prompt |
