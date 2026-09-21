# Coding standards

本 repo 的硬性编码约束。这些是「必须」，不是建议：**AstrBot 插件市场（AstrBot Cloud）上架时的自动安全
检查会逐条核对，违反任一条都会被拒绝上架。** 新增代码前先读这一页。

约束由 `tests/test_coding_standards.py` 自动检查（AST 扫描，不受注释与字符串影响）。

## 日志：只能从 `astrbot.api` 导入 logger

**规则**

- 记录日志必须使用 `from astrbot.api import logger`。
- 严禁 `import logging`、`from logging import ...`、`logging.getLogger(...)` 等任何 Python 内置
  `logging` 模块的用法。
- 不需要日志的文件不要引入 logger。

**理由**

- AstrBot 的 logger 会按调用位置路由到当前插件的 logger，等级可在 WebUI 中按插件单独配置，不影响
  核心与其他插件；内置 `logging` 不走这套机制，会绕过插件的日志等级设置。
- 插件市场自动安全检查会拒绝使用内置 `logging` 的插件。审核反馈原文（2026 年 v1.1.0 提审）：

  > 日志记录器 logger 必须且只能从 astrbot.api 导入（`from astrbot.api import logger`），严禁使用
  > 内置 logging 模块。

- 上游依据：《AstrBot 插件开发指南》[开发原则](https://docs.astrbot.app/dev/star/plugin-new.html)
  要求「请务必使用 `from astrbot.api import logger` 来获取日志对象，而不是 `logging` 模块」。

**怎么做**

- `main.py`（AstrBot 适配层）直接 `from astrbot.api import logger` —— 这是本 repo 唯一该导入 logger 的地方。
- `app/` 下的纯逻辑模块**不导入 astrbot**（见下一节）：要么不记日志，要么把要记录的内容返回/抛出，
  交由 `main.py` 记录。
  - 反例：`app/service.py` 曾写 `logger = logging.getLogger(__name__)` 却从未调用。正确做法是**直接删除**，
    而不是改成 `from astrbot.api import logger`（后者会把 astrbot 依赖带进 `app/`）。

## `app/` 层不依赖 astrbot

- `main.py` 是唯一接触 AstrBot API 的地方：`astrbot.api.*`、`filter` 装饰器、插件 `config`、`logger`。
- `app/` 下的模块只做纯逻辑，**不得 `import astrbot`**。
- 为什么：`app/` 的单元测试在未安装 AstrBot 的环境（CI、本机）也能直接跑。一旦 `app/` 依赖 astrbot，
  整套测试就只能塞进 AstrBot 运行时里跑，`python -m pytest` 会直接 ImportError。
- 需要 AstrBot 能力（配置、日志、事件）时，由 `main.py` 读取后以参数传给 `app/`（例如
  `GameDownloadService(config, cache)`）。

## 其他上架相关约束

《AstrBot 插件开发指南》开发原则里与本 repo 相关的项：

| 约束 | 本 repo 的做法 |
| --- | --- |
| 网络请求不得使用 `requests`，应使用 `httpx`/`aiohttp` 等异步库 | 全部走 `httpx.AsyncClient`，集中在 `app/http_client.py` |
| 持久化数据存放于 `data` 目录，而非插件自身目录 | `data/plugin_data/astrbot_plugin_wanna_play_game/cache.json` |
| 良好的错误处理，不要让插件因单个错误而崩溃 | `main.py::_search_and_reply` 兜底；各来源解析失败降级为 `fallback_candidate` |
| 功能需经过测试 | `tests/`，`python -m pytest` |
| 提交前用 [ruff](https://docs.astral.sh/ruff/) 格式化 | 未纳入本地强制流程，提交前请自行执行 |

## 检查清单

发布新版本前：

1. `python -m pytest -q` 全绿（含 `tests/test_coding_standards.py` 的日志与分层约束）。
2. 确认没有新增 `import logging`（约束检查已覆盖）。
3. 确认 `app/` 下没有新增 `import astrbot`（约束检查已覆盖）。
4. 新增/变更的配置项同步更新 `_conf_schema.json` 与 `README.md` 的配置表。
5. 需要用户注意的行为变化，在 `README.md` 与 `docs/adr/` 中留痕。
