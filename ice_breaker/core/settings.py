import os

from dotenv import load_dotenv
from pydantic import BaseConfig

from ice_breaker.models.environment import Environment

load_dotenv()

DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class Settings(BaseConfig):
    # LinkedIn API (Proxycurl)
    environment = Environment(os.getenv("ENVIRONMENT", "development"))
    if os.getenv("ENVIRONMENT") == "production":
        linkedin_api_endpoint = os.getenv("PROXYCURL_API_ENDPOINT")
        linkedin_api_key = os.getenv("PROXYCURL_API_KEY")
    else:
        path_to_linkedin_sample_profile = os.path.join(DIR, "test", "linkedin_sample_profile.json")


def get_settings(item: str):
    settings = Settings()
    return getattr(settings, item)
