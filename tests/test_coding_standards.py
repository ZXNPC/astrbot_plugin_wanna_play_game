"""固化 docs/agents/coding-standards.md 中的硬性约束。

插件市场自动安全检查会拒绝使用内置 logging 的插件，因此这些约束必须由测试兜住。
用 AST 扫描而非文本匹配，避免被注释/字符串里的 "logging" 误伤。
"""

import ast
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKIP_DIRS = {"data", "__pycache__"}


def _python_files():
    return [
        path
        for path in REPO.rglob("*.py")
        if not any(
            part in SKIP_DIRS or part.startswith(".")
            for part in path.relative_to(REPO).parts
        )
    ]


def _stdlib_logging_imports(tree: ast.AST) -> list[int]:
    lines = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(
                alias.name == "logging" or alias.name.startswith("logging.")
                for alias in node.names
            ):
                lines.append(node.lineno)
        elif isinstance(node, ast.ImportFrom):
            # from logging import ... / from logging.handlers import ...
            if node.module == "logging" or (node.module or "").startswith("logging."):
                lines.append(node.lineno)
    return lines


def test_no_stdlib_logging_imports():
    offenders = [
        f"{path.relative_to(REPO)}:{lineno}"
        for path in _python_files()
        for lineno in _stdlib_logging_imports(
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        )
    ]
    assert offenders == [], (
        "必须使用 from astrbot.api import logger，严禁内置 logging 模块："
        + ", ".join(offenders)
    )


def test_app_layer_does_not_import_astrbot():
    offenders = []
    for path in (REPO / "app").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                if any(alias.name.split(".")[0] == "astrbot" for alias in node.names):
                    offenders.append(f"{path.relative_to(REPO)}:{node.lineno}")
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0 and (node.module or "").split(".")[0] == "astrbot":
                    offenders.append(f"{path.relative_to(REPO)}:{node.lineno}")
    assert offenders == [], (
        "app/ 是纯逻辑层，不得依赖 astrbot（否则单元测试无法脱离 AstrBot 运行）："
        + ", ".join(offenders)
    )
