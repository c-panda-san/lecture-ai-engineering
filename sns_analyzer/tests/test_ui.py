import pytest
from unittest.mock import MagicMock, patch
import ui


def test_dashboard(monkeypatch):
    mock_st = MagicMock()
    monkeypatch.setattr("ui.st", mock_st)
    ui.dashboard()
    mock_st.title.assert_called_with("SNSソーシャルリスニング ダッシュボード")
    mock_st.write.assert_called()
    mock_st.markdown.assert_called()
    mock_st.button.assert_called()


def test_create_job_input_validation(monkeypatch):
    mock_st = MagicMock()
    monkeypatch.setattr("ui.st", mock_st)

    # 例えば、キーワード空の場合のエラー表示をテスト
    mock_st.text_input.return_value = ""
    mock_st.date_input.side_effect = [  # 開始日、終了日
        # 開始日 > 終了日のケースもテスト可能
    ]

    ui.create_job()

    mock_st.error.assert_called_with("キーワードを入力してください。")
