"""触发入口解析：`/game` 命令与「我想玩 xxx」自然语言表达。"""

from __future__ import annotations

import re

# 自然语言入口：我想玩 X / 我要玩 X
NL_PATTERN = r"^(?:我想玩(?:一下)?|我要玩)\s*[:：]?\s*(.+?)[。！？!?.,，\s]*$"
NL_REGEX = re.compile(NL_PATTERN)
# AstrBot 会剥掉 wake_prefix（默认 "/"），所以指令正文可能是 "game xxx" 或 "/game xxx"
CMD_REGEX = re.compile(r"^(?:/)?game\s+(.+?)\s*$", re.IGNORECASE)


def parse_command_text(text: str) -> str:
    """取 `/game <游戏名>` 中的游戏名；不是 game 指令或没有参数时返回空串。"""
    match = CMD_REGEX.match((text or "").strip())
    return match.group(1).strip() if match else ""


def parse_natural_language_text(text: str) -> str:
    """取「我想玩 <游戏名>」「我要玩 <游戏名>」中的游戏名；不匹配时返回空串。

    该模式无法区分「我想玩赛博朋克2077」与「我想玩点好玩的」（后者会被解析成
    「点好玩的」），因此调用方只在配置项 `enable_nl_trigger` 开启时才使用本函数结果。
    """
    match = NL_REGEX.search((text or "").strip())
    return match.group(1).strip() if match else ""
