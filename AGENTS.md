## Agent skills

### Issue tracker

Issues 和 specs 存放在 GitHub Issues，使用 `gh` CLI。See `docs/agents/issue-tracker.md`.

### Triage labels

默认五个 canonical triage labels：`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human`、`wontfix`。See `docs/agents/triage-labels.md`.

### Domain docs

Single-context：repo 根目录 `CONTEXT.md` + `docs/adr/`。See `docs/agents/domain.md`.

### Coding standards

硬性约束，违反会被 AstrBot 插件市场拒绝上架：日志只能 `from astrbot.api import logger`（严禁内置 `logging`），`app/` 层不得 `import astrbot`。See `docs/agents/coding-standards.md`.
