# llm.py

# 意味検索
from sentence_transformers import SentenceTransformer, util

# セマンティック検索用モデル
semantic_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


def semantic_search(posts, keyword, top_k=10):
    if not posts:
        return []

    texts = [p["title"] + " " + (p.get("selftext") or "") for p in posts]

    if not texts:
        return []

    post_vecs = semantic_model.encode(texts, convert_to_tensor=True)
    query_vec = semantic_model.encode(keyword, convert_to_tensor=True)

    if post_vecs.shape[0] == 0:
        return []

    cos_scores = util.cos_sim(query_vec, post_vecs)[0]
    top_results = cos_scores.argsort(descending=True)[:top_k]
    return [posts[i] for i in top_results]


def analyze_sentiment(posts, lang="auto"):
    from textblob import TextBlob

    results = []
    for post in posts:
        text = post["title"] + " " + (post["selftext"] or "")
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        results.append({"text": text, "sentiment": sentiment, "url": post["url"]})
    return results
