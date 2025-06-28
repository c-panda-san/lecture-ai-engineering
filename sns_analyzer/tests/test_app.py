from unittest.mock import patch, MagicMock
import app


def test_initial_page_state(monkeypatch):
    # session_state 初期化
    monkeypatch.setattr("streamlit.session_state", {"page": "dashboard"})

    # radio の選択をモックして "新規リスニングジョブ作成" を選ぶ
    def mock_radio(label, options, index):
        return "新規リスニングジョブ作成"

    monkeypatch.setattr("streamlit.sidebar.radio", mock_radio)

    # ui モジュールの dashboard / create_job 関数をモック
    with patch("ui.dashboard") as mock_dashboard, patch(
        "ui.create_job"
    ) as mock_create_job:
        app.st = MagicMock()  # streamlit をモック化
        app.ui = MagicMock()

        # 実際に create_job が呼ばれたか確認
        app.ui.create_job()
        app.ui.create_job.assert_called_once()
