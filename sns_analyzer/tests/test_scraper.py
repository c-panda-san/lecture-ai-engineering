# sns_analyzer/tests/test_scraper.py

from unittest.mock import MagicMock, patch
from sns_analyzer.scr import scraper


@patch("sns_analyzer.scr.scraper.praw.Reddit")
def test_fetch_reddit_posts(mock_reddit_class):
    # Mocked Reddit post
    mock_post = MagicMock()
    mock_post.title = "Test Title"
    mock_post.selftext = "Test Body"
    mock_post.url = "http://example.com"
    mock_post.score = 100
    mock_post.created_utc = 1234567890

    # Configure mock Reddit object
    mock_reddit = MagicMock()
    mock_reddit.subreddit.return_value.search.return_value = [mock_post]
    mock_reddit_class.return_value = mock_reddit

    posts = scraper.fetch_reddit_posts(
        keyword="test",
        client_id="fake_id",
        client_secret="fake_secret",
        user_agent="fake_agent",
    )

    assert isinstance(posts, list)
    assert len(posts) == 1
    assert posts[0]["title"] == "Test Title"
