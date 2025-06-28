from unittest.mock import MagicMock
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

    # エラー検出のために、キーワードと日付をモック
    mock_st.text_input.return_value = ""  # 空キーワード
    mock_st.date_input.side_effect = [
        # 開始日 > 終了日 の状態をシミュレーション（例えば today, today - 1）
        ui.datetime.date.today(),
        ui.datetime.date.today() - ui.datetime.timedelta(days=1),
    ]
    mock_st.selectbox.side_effect = ["感情分析（ポジ/ネガ判定）", "Reddit", "棒グラフ"]
    mock_st.button.return_value = True  # 「取得開始」が押されたことにする

    ui.create_job()

    # エラーが呼ばれていることを確認
    mock_st.error.assert_any_call("キーワードを入力してください。")
    mock_st.error.assert_any_call("開始日は終了日より前に設定してください。")
