from typing import Union

from ice_breaker.core.log import logger
from ice_breaker.services.abstract_service import AbstractService


class TwitterService(AbstractService):
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
        # TODO: Implement the Twitter profile scraping
        return {"a": "b"}

    def _clean_profile(self, profile_data: dict[str, Union[str, dict[str, str]]]) -> dict[str, Union[str, dict[str, str]]]:
        """
        Cleans the LinkedIn profile information. Removes empty and unnecessary fields.

        :param profile_data: The LinkedIn profile information as a dictionary.
        :return: The cleaned LinkedIn profile information as a dictionary.
        """
        # Keeping only the needed fields
        linkedin_profile_clean = {
            k: v
            for k, v in profile_data.items()
            if v not in ["", [], None] and k not in ["people also viewed", "certifications"]
        }

        # Remove profile_pic_url from groups
        if linkedin_profile_clean["groups"] and isinstance(linkedin_profile_clean["groups"], list):
            for group_dict in linkedin_profile_clean["groups"]:
                if "profile_pic_url" in group_dict:
                    group_dict.pop("profile_pic_url")

        return linkedin_profile_clean
