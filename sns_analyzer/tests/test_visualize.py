# sns_analyzer/tests/test_visualize.py

from sns_analyzer.scr import visualize


def test_plot_wordcloud_runs(monkeypatch):
    # モック Streamlit と plt の描画関数（st.pyplotなど）
    class DummyStreamlit:
        def pyplot(self, *args, **kwargs):
            pass

    monkeypatch.setitem(visualize.__dict__, "st", DummyStreamlit())

    sample_texts = ["hello", "world", "streamlit", "test"]
    try:
        visualize.plot_wordcloud(sample_texts)
    except Exception:
        assert False, "plot_wordcloud raised an unexpected exception"
