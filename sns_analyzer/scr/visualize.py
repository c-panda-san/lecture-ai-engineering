# visualize.py
import os

def plot_wordcloud(texts, width=400, height=200):
    import streamlit as st
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    text = " ".join(texts)

    # GitHub同梱のフォントを優先使用
    font_path = os.path.join(os.path.dirname(__file__), "..", "fonts", "NotoSansCJKjp-Regular.otf")
    if not os.path.exists(font_path):
        font_path = None  # fallback（英語のみ）

    wordcloud = WordCloud(
        width=width,
        height=height,
        font_path=font_path,
        background_color="white"
    ).generate(text)

    fig, ax = plt.subplots(figsize=(width / 100, height / 100))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
