import json
from pathlib import Path

SCHEMA = json.loads(
    (Path(__file__).resolve().parents[1] / "_conf_schema.json").read_text(encoding="utf-8")
)


def test_nl_trigger_option_exists():
    assert "enable_nl_trigger" in SCHEMA


def test_nl_trigger_defaults_to_off():
    # 默认关闭：用户没配置时「我想玩 xxx」不触发检索。
    assert SCHEMA["enable_nl_trigger"]["type"] == "bool"
    assert SCHEMA["enable_nl_trigger"]["default"] is False
