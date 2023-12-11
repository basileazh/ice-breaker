# Description: Scrapes Twitter data using Apify.
# UI on website : https://console.apify.com/actors/runs

import os

from apify_client import ApifyClient

from ice_breaker.core.log import logger
from ice_breaker.core.settings import get_settings

apify_client = ApifyClient(os.getenv("APIFY_API_KEY"))


def scrape_user_profile(username: str) -> dict[str, dict[str, str]]:
    """
    Scrape user information from a username.

    :param username: The user's username.
    :return: Data about the user.
    """
    logger.info(f"Scraping Twitter data for {username}...")

    # # Start an actor and wait for it to finish
    # actor_call = apify_client.actor("quacker/twitter-scraper").call(
    #     run_input={
    #         "addUserInfo": True,
    #         "collectOriginalTweetOnly": False,
    #         "debugLog": False,
    #         "includeThreadsOnly": False,
    #         "mode": "own",
    #         "profilesDesired": 10,
    #         "proxyConfig": {"useApifyProxy": True},
    #         "repliesDepth": 0,
    #         "searchMode": "live",
    #         "skipRetweets": True,
    #         "startUrls": [{"url": f"https://twitter.com/{username}"}],
    #         "tweetsDesired": 10,
    #         "useAdvancedSearch": False,
    #     },
    #     content_type="application/json",
    # )
    #
    # # Fetch results from the actor run's default dataset
    # dataset_items = (
    #     apify_client.dataset(actor_call["defaultDatasetId"]).list_items().items[0]
    # )
    #
    # logger.info(f"Raw Twitter data : {dataset_items}.")
    #
    # import json
    # with open("outputs/twitter_data.json", "w", encoding="utf-8") as f:
    #     json.dump(dataset_items, f, ensure_ascii=False, indent=4)

    # Load the data from the file
    import json

    with open("outputs/twitter_data.json", encoding="utf-8") as f:
        dataset_items = json.load(f)

    # keeping only the needed fields
    filtered_dataset_items = {
        "user": {k: dataset_items["user"][k] for k in get_settings("twitter_fields_user")},
        "pinned_tweet": {k: dataset_items[k] for k in get_settings("twitter_fields_pinned_tweet")},
    }

    logger.info(f"Scraped Twitter data for {username}.")

    return filtered_dataset_items
