# Description: Scrapes Twitter data using Apify.
# UI on website : https://console.apify.com/actors/runs

import json

from apify_client import ApifyClient

from ice_breaker.core.log import logger
from ice_breaker.core.settings import get_settings
from ice_breaker.models.environment import Environment

path_to_twitter_sample_profile_default = get_settings("path_to_twitter_sample_profile")


def scrape_twitter_profile(username: str, mode: str = "development") -> dict[str, dict[str, str]]:
    """
    Scrapes a Twitter profile and pinned tweet and returns the information as a dictionary.

    :param username: The LinkedIn profile URL to scrape. Only used for Production mode
    :param mode: The mode to use. Can be either "development" or "production".
        dev: Uses the local default file to retrieve the LinkedIn profile.
        prod: Uses the ProxyCurl API to retrieve the LinkedIn profile.
    :return: A dict containing the LinkedIn profile information.
    """
    mode = Environment(mode)
    if mode == "development":
        twitter_profile = _scrape_twitter_profile_development()
    elif mode == "production":
        if not username:
            raise ValueError("twitter_profile_url must be provided in production mode, here is it empty")
        twitter_profile = _scrape_twitter_profile_production(username=username)
    else:
        raise ValueError(f"Invalid mode: {mode}")

    # Remove empty and unnecessary fields
    twitter_profile_clean = clean_twitter_profile(twitter_profile)

    return twitter_profile_clean


def _scrape_twitter_profile_production(username: str) -> dict[str, dict[str, str]]:
    """
    Scrape user information from a username.

    :param username: The user's username.
    :return: Data about the user.
    """
    apify_client = ApifyClient(get_settings("twitter_apify_api_key"))

    logger.info(f"Scraping Twitter data for {username}...")

    # Start an actor and wait for it to finish
    actor_call = apify_client.actor(get_settings("apify_twitter_actor_id")).call(
        run_input={
            "addUserInfo": True,
            "collectOriginalTweetOnly": False,
            "debugLog": False,
            "includeThreadsOnly": False,
            "mode": "own",
            "profilesDesired": 10,
            "proxyConfig": {"useApifyProxy": True},
            "repliesDepth": 0,
            "searchMode": "live",
            "skipRetweets": True,
            "startUrls": [{"url": f"https://twitter.com/{username}"}],
            "tweetsDesired": 10,
            "useAdvancedSearch": False,
        },
        content_type="application/json",
    )

    raw_twitter_data = apify_client.dataset(actor_call["defaultDatasetId"]).list_items().items

    logger.info(f"Raw Twitter data : {raw_twitter_data}.")

    # Fetch results from the actor run's default dataset
    dataset_items = raw_twitter_data[0]

    logger.info(f"Scraped Twitter data for {username}.")

    return dataset_items


def _scrape_twitter_profile_development(
    path_to_twitter_sample_profile=path_to_twitter_sample_profile_default,
) -> dict[str, dict[str, str]]:
    """
    Retrieves the local Twitter profile and returns the information as a dictionary.

    :param path_to_twitter_sample_profile: The path to the local Twitter profile.
    :return: A dict containing the Twitter profile information.
    """
    # Load the data from the file
    with open("outputs/twitter_sample_profile.json", encoding="utf-8") as f:
        dataset_items = json.load(f)

    return dataset_items


def clean_twitter_profile(twitter_profile: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    """
    Cleans the Twitter profile information.

    :param twitter_profile: The Twitter profile information to clean.
    :return: The cleaned Twitter profile information.
    """
    # Keeping only the needed fields
    filtered_twitter_profile = {
        "user": {k: twitter_profile["user"][k] for k in get_settings("twitter_fields_user")},
        "pinned_tweet": {k: twitter_profile[k] for k in get_settings("twitter_fields_pinned_tweet")},
    }

    return filtered_twitter_profile  # type: ignore


def download_twitter_profile(
    username: str, path: str = path_to_twitter_sample_profile_default, clean_profile: bool = True
) -> dict[str, dict[str, str]]:
    """
    Downloads a Twitter profile and pinned tweet and returns the information as a dictionary.

    :param username: The LinkedIn profile URL to scrape. Only used for Production mode
    :param path: The path to the local Twitter profile.
    :param clean_profile: Whether to clean the profile or not
    :return: A dict containing the LinkedIn profile information.
    """
    # Scrape the Twitter profile
    twitter_profile = _scrape_twitter_profile_production(username=username)

    if clean_profile:
        # Remove empty and unnecessary fields
        twitter_profile = clean_twitter_profile(twitter_profile)

    # Save the data to the file
    with open(path, "w", encoding="utf-8") as f:
        json.dump(twitter_profile, f, ensure_ascii=False, indent=4)

    return twitter_profile
