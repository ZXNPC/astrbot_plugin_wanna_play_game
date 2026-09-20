from app.trigger import parse_command_text, parse_natural_language_text


def test_parse_command_text_accepts_bare_and_slashed_forms():
    assert parse_command_text("game 赛博朋克2077") == "赛博朋克2077"
    assert parse_command_text("/game 赛博朋克2077") == "赛博朋克2077"
    assert parse_command_text("/Game Cyberpunk 2077") == "Cyberpunk 2077"


def test_parse_command_text_returns_empty_without_game_name():
    assert parse_command_text("/game") == ""
    assert parse_command_text("game") == ""
    assert parse_command_text("") == ""


def test_parse_command_text_keeps_cache_clear_phrase():
    assert parse_command_text("/game 清空游戏检索缓存") == "清空游戏检索缓存"


def test_parse_command_text_trims_whitespace():
    assert parse_command_text("  /game   黑神话悟空  ") == "黑神话悟空"


def test_parse_natural_language_text_extracts_game_name():
    assert parse_natural_language_text("我想玩赛博朋克2077") == "赛博朋克2077"
    assert parse_natural_language_text("我要玩黑神话悟空！") == "黑神话悟空"
    assert parse_natural_language_text("我想玩一下：艾尔登法环") == "艾尔登法环"


def test_parse_natural_language_text_ignores_unrelated_messages():
    assert parse_natural_language_text("今天天气不错") == ""
    assert parse_natural_language_text("/game 赛博朋克2077") == ""
    assert parse_natural_language_text("") == ""


def test_parse_natural_language_text_documents_chatter_false_positive():
    # 「我想玩点好玩的」会被解析成「点好玩的」——这正是自然语言入口默认关闭的原因。
    assert parse_natural_language_text("我想玩点好玩的") == "点好玩的"
