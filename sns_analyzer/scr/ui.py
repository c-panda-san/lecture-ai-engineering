import streamlit as st
import datetime
import config
from llm import analyze_sentiment, semantic_search
from visualize import plot_wordcloud
import traceback
import matplotlib.pyplot as plt


def dashboard():
    st.title("SNSソーシャルリスニング ダッシュボード")
    st.write("サービス概要")
    st.markdown(
        """
- SNSや口コミサイトから世の中の声を簡単に分析できます。
- 新規リスニングジョブを作成し、調査結果を取得してください。
    """
    )
    if st.button("新規リスニングジョブ作成"):
        st.session_state["page"] = "create_job"
        st.rerun()


def create_job():
    st.title("新規リスニングジョブ作成")
    st.caption(
        "※検索では最大100件のReddit投稿から、関連性の高い投稿を抽出します。期間やキーワードによっては少数の結果になる場合があります。"
    )
    keyword = st.text_input("キーワード", key="keyword")
    st.caption(
        "※現在、感情分析は英語投稿のみに対応しています。日本語投稿はneutralと判定される可能性があります。"
    )

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "開始日",
            value=datetime.date.today() - datetime.timedelta(days=30),
            key="start_date",
        )
    with col2:
        end_date = st.date_input("終了日", value=datetime.date.today(), key="end_date")
    analysis_method = st.selectbox("分析手法", ["感情分析（ポジ/ネガ判定）"])
    st.write(f"選択された分析手法: {analysis_method}")
    sns_type = st.selectbox("対象SNS", ["Reddit"])
    st.write(f"選択された対象SNS: {sns_type}")
    output_format = st.selectbox(
        "出力形式",
        ["棒グラフ", "円グラフ", "WordCloud", "テキスト（箇条書き）"],
        key="output_format",
    )
    st.caption("※出力形式は、再取得せずに切り替えることができます。")

    if st.button("取得開始"):
        error_flag = False

        if not keyword:
            st.error("キーワードを入力してください。")
            error_flag = True
        if start_date > end_date:
            st.error("開始日は終了日より前に設定してください。")
            error_flag = True

        reddit_client_id = config.REDDIT_CLIENT_ID
        reddit_client_secret = config.REDDIT_CLIENT_SECRET
        reddit_user_agent = config.REDDIT_USER_AGENT

        if not reddit_client_id or not reddit_client_secret or not reddit_user_agent:
            st.error(
                "Reddit API認証情報が設定されていません。.envファイルを確認してください。"
            )
            error_flag = True

        if not error_flag:
            st.session_state["job_started"] = True
            st.session_state["job_params"] = {
                "keyword": keyword,
                "start_date": start_date,
                "end_date": end_date,
                "output_format": output_format,
            }
        else:
            st.session_state["job_started"] = False

    if st.session_state.get("job_started", False):
        from scraper import fetch_reddit_posts

        params = st.session_state["job_params"]
        try:
            posts = fetch_reddit_posts(
                params["keyword"],
                config.REDDIT_CLIENT_ID,
                config.REDDIT_CLIENT_SECRET,
                config.REDDIT_USER_AGENT,
                limit=100,
            )

            if not posts:
                st.session_state["last_results"] = {
                    "message": "投稿が見つかりませんでした。"
                }
                st.info(
                    "※指定キーワードに関連する投稿が期間内に見つからなかったか、最大取得数（100件）に含まれていなかった可能性があります。"
                )
            else:
                semantic_filtered_posts = semantic_search(
                    posts, params["keyword"], top_k=100
                )
                start_ts = datetime.datetime.combine(
                    params["start_date"], datetime.time.min
                ).timestamp()
                end_ts = datetime.datetime.combine(
                    params["end_date"], datetime.time.max
                ).timestamp()
                date_filtered_posts = [
                    p
                    for p in semantic_filtered_posts
                    if start_ts <= p["created_utc"] <= end_ts
                ]

                if not date_filtered_posts:
                    st.session_state["last_results"] = {
                        "message": "投稿が見つかりませんでした。"
                    }
                else:
                    sentiment_results = analyze_sentiment(
                        date_filtered_posts, lang="auto"
                    )
                    st.session_state["last_results"] = {
                        "filtered_posts": date_filtered_posts,
                        "sentiment_results": sentiment_results,
                    }

        except Exception as e:
            st.session_state["last_results"] = {
                "error": str(e),
                "trace": traceback.format_exc(),
            }

        st.session_state["job_started"] = False

    last_results = st.session_state.get("last_results")
    if last_results and "sentiment_results" in last_results:
        sentiment_results = last_results["sentiment_results"]
        pos = sum(1 for r in sentiment_results if r["sentiment"] == "positive")
        neg = sum(1 for r in sentiment_results if r["sentiment"] == "negative")
        neu = sum(1 for r in sentiment_results if r["sentiment"] == "neutral")
        total = len(sentiment_results)
        output_format = st.session_state.get("output_format", "棒グラフ")

        st.markdown("### Reddit投稿の感情分析結果")

        if output_format == "棒グラフ":
            st.bar_chart({"positive": pos, "negative": neg, "neutral": neu})

        elif output_format == "円グラフ":
            labels = ["positive", "negative", "neutral"]
            sizes = [pos, neg, neu]
            fig, ax = plt.subplots(figsize=(1, 1))  # ← サイズ拡大
            wedges, texts, autotexts = ax.pie(
                sizes,
                labels=labels,
                autopct="%1.1f%%",
                textprops={"fontsize": 4},  # ← 注釈の文字サイズ指定
            )
            ax.axis("equal")
            st.pyplot(fig)

        elif output_format == "WordCloud":
            positive_texts = [
                res["text"]
                for res in sentiment_results
                if res["sentiment"] == "positive"
            ]
            negative_texts = [
                res["text"]
                for res in sentiment_results
                if res["sentiment"] == "negative"
            ]
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### ポジティブな投稿のワードクラウド")
                if positive_texts:
                    plot_wordcloud(positive_texts, width=300, height=150)
                else:
                    st.write("ポジティブな投稿がありません。")
            with col2:
                st.markdown("#### ネガティブな投稿のワードクラウド")
                if negative_texts:
                    plot_wordcloud(negative_texts, width=300, height=150)
                else:
                    st.write("ネガティブな投稿がありません。")

        else:
            st.markdown(f"- ポジティブ: {pos}件 ({pos/total*100:.1f}%)")
            st.markdown(f"- ネガティブ: {neg}件 ({neg/total*100:.1f}%)")
            st.markdown(f"- ニュートラル: {neu}件 ({neu/total*100:.1f}%)")

        st.markdown("#### 投稿（出所付き）")
        for res in sentiment_results:
            st.markdown(
                f"- {res['text'][:60]}... ({res['sentiment']}) [出所]({res['url']})"
            )

    elif last_results and "error" in last_results:
        st.error(f"Reddit APIでエラーが発生しました: {last_results['error']}")
        st.code(last_results.get("trace", ""))
    elif last_results and "message" in last_results:
        st.warning(last_results["message"])
