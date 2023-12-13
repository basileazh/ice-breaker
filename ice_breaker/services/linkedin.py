import json

import requests  # type: ignore[import]

from ice_breaker.core.settings import get_settings
from ice_breaker.models.environment import Environment

path_to_linkedin_sample_profile_default = get_settings("path_to_linkedin_sample_profile")


def scrape_linkedin_profile(linkedin_profile_url="", mode: str = "development") -> dict[str, str]:
    """
    Scrapes a LinkedIn profile and returns the information as a dictionary.

    :param linkedin_profile_url: The LinkedIn profile URL to scrape. Only used for Production mode
    :param mode: The mode to use. Can be either "development" or "production".
        dev: Uses the local default file to retrieve the LinkedIn profile.
        prod: Uses the ProxyCurl API to retrieve the LinkedIn profile.
    :return: A dict containing the LinkedIn profile information.
    """
    mode = Environment(mode)
    if mode == "development":
        linkedin_profile = _scrape_linkedin_profile_development()
    elif mode == "production":
        if not linkedin_profile_url:
            raise ValueError("linkedin_profile_url must be provided in production mode, here is it empty")
        linkedin_profile = _scrape_linkedin_profile_production(linkedin_profile_url)
    else:
        raise ValueError(f"Invalid mode: {mode}")

    # Remove empty and unnecessary fields
    linkedin_profile_clean = clean_linkedin_profile(linkedin_profile)

    return linkedin_profile_clean


def _scrape_linkedin_profile_production(linkedin_profile_url: str) -> dict[str, str]:
    """
    Scrapes a LinkedIn profile and returns the information as a dictionary.

    :param linkedin_profile_url: The LinkedIn profile URL to scrape.
    :return: A dict containing the LinkedIn profile information.
    """
    linkedin_api_endpoint = get_settings("linkedin_api_endpoint")
    linkedin_api_key = get_settings("linkedin_api_key")

    header_dict = {
        "Authorization": f"Bearer {linkedin_api_key}",
        "Content-Type": "application/json",
    }

    response = requests.get(
        linkedin_api_endpoint,
        headers=header_dict,
        params={"url": linkedin_profile_url},
    )

    return response.json()


def _scrape_linkedin_profile_development(
    path_to_linkedin_sample_profile: str = path_to_linkedin_sample_profile_default,
) -> dict[(str, str)]:
    """
    Retrieves the local LinkedIn profile and returns the information as a dictionary.

    :param path_to_linkedin_sample_profile: The path to the local LinkedIn profile.
    :return: A dict containing the LinkedIn profile information.
    """
    import json

    with open(path_to_linkedin_sample_profile) as f:
        return json.load(f)


def clean_linkedin_profile(linkedin_profile: dict[str, str]) -> dict[str, str]:
    """
    Cleans the LinkedIn profile information.

    :param linkedin_profile: The LinkedIn profile information to clean.
    :return: The cleaned LinkedIn profile information.
    """
    linkedin_profile_clean = {
        k: v
        for k, v in linkedin_profile.items()
        if v not in ["", [], None] and k not in ["people also viewed", "certifications"]
    }

    if linkedin_profile_clean["groups"] and isinstance(linkedin_profile_clean["groups"], list):
        for group_dict in linkedin_profile_clean["groups"]:
            group_dict.pop("profile_pic_url")

    return linkedin_profile_clean


def download_linkedin_profile(
    linkedin_profile_url: str, path: str = path_to_linkedin_sample_profile_default, clean_profile: bool = True
) -> dict[str, str]:
    """
    Downloads a LinkedIn profile and returns the information as a dictionary.

    :param linkedin_profile_url: The LinkedIn profile URL to scrape.
    :param path: The path to the local LinkedIn profile.
    :param clean_profile: Whether to clean the profile or not
    :return: A dict containing the LinkedIn profile information.
    """
    # Scrape the LinkedIn profile
    linkedin_profile = _scrape_linkedin_profile_production(linkedin_profile_url)

    if clean_profile:
        # Clean the LinkedIn profile
        linkedin_profile = clean_linkedin_profile(linkedin_profile)

    # Save the data to a file
    with open(path, "w") as f:
        json.dump(linkedin_profile, f)

    return linkedin_profile
