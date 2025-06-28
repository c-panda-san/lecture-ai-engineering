# sns_analyzer/tests/test_config.py

import sns_analyzer.scr.config as config


def test_config_values_exist():
    assert hasattr(config, "REDDIT_CLIENT_ID")
    assert hasattr(config, "REDDIT_CLIENT_SECRET")
    assert hasattr(config, "REDDIT_USER_AGENT")
