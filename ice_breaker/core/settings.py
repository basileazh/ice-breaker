import logging
import os

from dotenv import load_dotenv
from pydantic import BaseConfig

from ice_breaker.models.environment import Environment

load_dotenv()

DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

logging.basicConfig(level=logging.INFO)


class Settings(BaseConfig):
    # Logging
    log_file_path = "outputs/logs/[DATETIME_PLACEHOLDER]_log.txt"
    log_file_path_datetime_format = "%Y-%m-%d_%H"
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # LinkedIn API (Proxycurl)
    environment = Environment(os.getenv("ENVIRONMENT", "development"))
    if os.getenv("ENVIRONMENT") == "production":
        linkedin_api_endpoint = os.getenv("PROXYCURL_API_ENDPOINT")
        linkedin_api_key = os.getenv("PROXYCURL_API_KEY")
    else:
        path_to_linkedin_sample_profile = os.path.join(DIR, "test", "linkedin_sample_profile.json")

    # Twitter API (Apify)
    twitter_fields_user = [
        "name",
        "description",
        "followers_count",
        "friends_count",
        "profile_image_url_https",
        "verified",
    ]
    twitter_fields_pinned_tweet = [
        "full_text",
        "retweet_count",
        "favorite_count",
        "reply_count",
    ]


def get_settings(item: str):
    settings = Settings()
    return getattr(settings, item)
