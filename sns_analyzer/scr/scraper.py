# scraper.py
import praw

def fetch_reddit_posts(keyword, client_id, client_secret, user_agent, limit=50):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )
    subreddit = reddit.subreddit("all")
    posts = subreddit.search(keyword, limit=limit)
    results = []
    for post in posts:
        results.append({
            "title": post.title,
            "selftext": post.selftext,
            "url": post.url,
            "score": post.score,
            "created_utc": post.created_utc
        })
    return results
