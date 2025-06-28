import pytest
from unittest.mock import patch, MagicMock
import app


def test_initial_page_state(monkeypatch):
    # session_state初期化
    monkeypatch.setattr("streamlit.session_state", {"page": "dashboard"})

    # radioの選択をモックして"新規リスニングジョブ作成"を選ぶ
    def mock_radio(label, options, index):
        return "新規リスニングジョブ作成"

    monkeypatch.setattr("streamlit.sidebar.radio", mock_radio)

    # uiモジュールのdashboard/create_job関数をモック
    with patch("ui.dashboard") as mock_dashboard, patch(
        "ui.create_job"
    ) as mock_create_job:
        # 実行してcreate_jobが呼ばれることを確認
        app.st = MagicMock()  # streamlitをモック化
        app.ui = MagicMock()
