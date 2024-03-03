import re
from typing import Union

import requests  # type: ignore

from ice_breaker.core.log import logger
from ice_breaker.core.settings import get_settings
from ice_breaker.services.abstract_service import AbstractService

CLEAN_FIELDS = [
    "public_identifier",
    "profile_pic_url",
    "first_name",
    "last_name",
    "full_name",
    "headline",
    "country",
    "follower_count",
    "summary",
    "country_full_name",
    "city",
    "state",
    "experiences",
    "languages",
    "education",
    "skills",
]


class LinkedInService(AbstractService):
    """
    LinkedIn service class for scraping LinkedIn profiles.

    Implements the abstract methods:
    - _scrape_profile_production
    - _clean_profile
    - _clean_profile_slug

    Usage:
    - Manage the LinkedIn profile scraping
    - Download_profile_cli, the CLI command to download a LinkedIn profile
    - Use the service class in the CLI or in the API

    Example:
    >>> from ice_breaker.services.linkedin_service import LinkedInService
    >>> service = LinkedInService("https://www.linkedin.com/in/roberto-romano-4a5a8a1b/", "production")
    >>> service.scrape_profile()
    >>> service.save_profile()
    """

    def __init__(self, profile_id: str, environment: str = "development", profiles_path: str = ""):
        super().__init__(profile_id, environment, profiles_path)

        # Set the service name
        logger.info("Setting up LinkedIn service...")
        self.service_name = "linkedin"

    def _scrape_profile_production(self) -> dict[str, Union[str, dict[str, str]]]:
        """
        Retrieves the LinkedIn profile and returns the information as a dictionary.

        :return: The LinkedIn profile information as a dictionary.
        """

        # Trying to load the profile from the database
        try:
            profile = self.load_profile()
            logger.info(f"Profile {self.profile_id} found in the database.")
        except FileNotFoundError:
            logger.info(f"Profile {self.profile_id} not found in the database. Scraping it from LinkedIn...")
            logger.info(f"Scraping {self.profile_id} profile from LinkedIn via ProxyCurl...")

            # Get the LinkedIn api endpoint and key
            linkedin_api_endpoint = get_settings("linkedin_api_endpoint")
            linkedin_api_key = get_settings("linkedin_api_key")

            # Set the header
            header_dict = {
                "Authorization": f"Bearer {linkedin_api_key}",
                "Content-Type": "application/json",
            }

            # Get the profile data from the API
            response = requests.get(
                linkedin_api_endpoint,
                headers=header_dict,
                params={"url": self.profile_id},
            )

            profile = response.json()

        return profile

    def _clean_profile(self, profile_data: dict[str, Union[str, dict[str, str]]]) -> dict[str, Union[str, dict[str, str]]]:
        """
        Cleans the LinkedIn profile information. Removes empty and unnecessary fields.

        :param profile_data: The LinkedIn profile information as a dictionary.
        :return: The cleaned LinkedIn profile information as a dictionary.
        """
        # Keeping only the needed fields
        linkedin_profile_clean = {k: v for k, v in profile_data.items() if v not in ["", [], None] and k in CLEAN_FIELDS}

        # Remove profile_pic_url from groups
        if "groups" in linkedin_profile_clean and isinstance(linkedin_profile_clean["groups"], list):
            for group_dict in linkedin_profile_clean["groups"]:
                if "profile_pic_url" in group_dict:
                    group_dict.pop("profile_pic_url")

        return linkedin_profile_clean

    def _clean_profile_slug(self, profile_slug: str) -> str:
        """
        Cleans the LinkedIn profile slug. Removes the URL and trailing slash to keep only the "ID" part.

        :param profile_slug: The LinkedIn profile slug.
        :return: The cleaned LinkedIn profile slug.
        """
        # Remove the URL
        clean_profile_slug = re.sub(r"^https_\w{2,3}_linkedin_\w{2,3}_in_", "", string=profile_slug)

        # Remove the trailing slash
        clean_profile_slug = clean_profile_slug.rstrip("/")

        self.clean_profile_slug = clean_profile_slug
        return clean_profile_slug
