import logging
import os

import tweepy

logger = logging.getLogger("twitter")

# Authenticate to Twitter
client = tweepy.Client(
    consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
    consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
)
# client = tweepy.Client(os.getenv('TWITTER_BEARER_TOKEN'))


def scrape_user_tweets(username: str):
    """
    Scrape user information from a username.

    :param username: The user's username.
    :return: Data about the user.
    """
    logger.info(f"Scraping {username}'s information from Twitter...")

    user = client.get_me()

    return user
