from sns_analyzer import llm


def test_semantic_search_basic():
    posts = [
        {"title": "I love pandas", "selftext": "They are cute"},
        {"title": "Python is great", "selftext": "especially for data science"},
    ]
    keyword = "panda"
    results = llm.semantic_search(posts, keyword)
    assert isinstance(results, list)
    assert len(results) <= 2
    for res in results:
        assert "title" in res


def test_analyze_sentiment():
    posts = [
        {"title": "I love pandas", "selftext": "", "url": "http://example.com"},
        {"title": "Pandas are terrible", "selftext": "", "url": "http://example.com"},
        {"title": "Just some neutral post", "selftext": "", "url": "http://example.com"},
    ]
    results = llm.analyze_sentiment(posts)
    assert isinstance(results, list)
    assert all("sentiment" in res for res in results)
    sentiments = {r["sentiment"] for r in results}
    assert sentiments.issubset({"positive", "negative", "neutral"})
