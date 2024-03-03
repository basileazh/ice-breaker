import json
import os
from typing import Optional, Union

from slugify import slugify  # type: ignore

from ice_breaker.core.log import logger
from ice_breaker.core.settings import get_settings

# Default values
DEFAULT_ENVIRONMENT = get_settings("environment")
DEFAULT_PROFILES_PATH = get_settings("profiles_path")


class AbstractService:
    """
    Abstract class for Twitter and LinkedIn scraping API services.

    Main methods:
    - scrape_profile
    - clean_profile
    - save_profile
    - load_profile

    Usage:
    - Create a new service class that inherits from this class and implements the abstract methods
    - Use the service class in the CLI or in the API

    To be implemented:
    - service_name
    - _scrape_profile_production
    - _clean_profile

    Optional:
    - _clean_profile_slug eventually
    """

    def __init__(
        self,
        profile_id: str,
        environment: Optional[str] = DEFAULT_ENVIRONMENT,
        profiles_path: Optional[str] = DEFAULT_PROFILES_PATH,
    ):
        """
        Initialize the service

        :param profile_id: The profile ID to scrape. LinkedIn profile URL or Twitter username.
        :param environment: The mode to use. Can be either "production" or "development".
        :param profiles_path: The path to the profile's folder.
        """
        logger.info(
            f"Service setting up with profile_id={profile_id}, "
            f"environment={environment}, "
            f"profiles_path={profiles_path}..."
        )
        self.profile_id = profile_id
        self.environment = environment if environment else DEFAULT_ENVIRONMENT
        self.profiles_path = profiles_path if profiles_path else DEFAULT_PROFILES_PATH
        self.service_name = ""  # To be implemented by the child class

        self.clean_profile_slug: str  # To be set by _clean_profile_slug
        self.profile_data: dict[str, Union[str, dict[str, str]]]  # To be set by scrape_profile
        self.profile_path: str  # To be set by _get_profile_path

    def _scrape_profile_production(self) -> dict[str, Union[str, dict[str, str]]]:
        """
        Retrieves the LinkedIn profile and returns the information as a dictionary.

        :return: A dict containing the LinkedIn profile information.
        """
        raise NotImplementedError

    def _scrape_profile_development(self) -> dict[str, Union[str, dict[str, str]]]:
        """
        Retrieves the local LinkedIn profile and returns the information as a dictionary.

        :return: A dict containing the LinkedIn profile information.
        """
        logger.info(f"Scraping {self.profile_id} profile from local...")
        # Load the data from the file
        profile_data = self._load_profile()

        return profile_data

    def scrape_profile(self, clean_profile: bool = True, force_scraping: bool = False) -> dict[str, Union[str, dict[str, str]]]:
        """
        Retrieves the profile and returns the information as a dictionary. Depending on the environment,
        the profile is either scraped or loaded from local.

        :param force_scraping: Whether to force the scraping using API or not
        :param clean_profile: Whether to clean the profile or not
        :return: A dict containing profile information.
        """
        logger.info(f"Scraping {self.profile_id} profile...")

        # Scrape the profile data depending on the environment
        if (self.environment == "production") | force_scraping:
            self.profile_data = self._scrape_profile_production()
        elif self.environment == "development":
            self.profile_data = self._scrape_profile_development()
        else:
            raise ValueError(f"Unknown environment '{self.environment}'")

        # Clean the profile
        if clean_profile:
            logger.info("Cleaning profile...")
            self.clean_profile()

        logger.info("Scraped profile data.")
        logger.debug(f"Scraped {self.profile_id} profile : {self.profile_data}.")

        return self.profile_data

    def _clean_profile(self, profile_data: dict[str, Union[str, dict[str, str]]]) -> dict[str, Union[str, dict[str, str]]]:
        """
        Cleans the profile information.

        :param profile_data: The profile information to clean.
        :return: The cleaned profile information.
        """
        raise NotImplementedError

    def clean_profile(
        self,
    ) -> dict[str, Union[str, dict[str, str]]]:
        """
        Cleans the profile information.

        :return: The cleaned profile information.
        """
        if not self.profile_data:
            raise ValueError("No profile data to clean")

        logger.info(f"Cleaning {self.profile_id} profile...")

        clean_profile_data = self._clean_profile(self.profile_data)
        self.profile_data = clean_profile_data

        logger.info("Cleaned profile data.")
        logger.debug(f"Cleaned {self.profile_id} profile : {clean_profile_data}.")

        return clean_profile_data

    def _save_profile(self, profile_data: dict[str, Union[str, dict[str, str]]]) -> dict[str, Union[str, dict[str, str]]]:
        """
        Saves the profile information.

        :param profile_data: The profile information to save.
        :return: The saved profile information.
        """
        # Save the data to file
        with open(self._get_profile_path(), mode="w+", encoding="utf-8") as f:
            json.dump(profile_data, f)

        return profile_data

    def save_profile(self) -> dict[str, Union[str, dict[str, str]]]:
        """
        Saves the profile information.

        :return: The saved profile information.
        """
        logger.info(f"Saving {self.profile_id} profile...")

        if self.profile_data:
            profile_data = self._save_profile(profile_data=self.profile_data)

            logger.info("Saved profile data.")
            logger.debug(f"Saved {self.profile_id} profile : {profile_data}.")

            return profile_data
        else:
            raise ValueError("No profile data to save")

    # def save_profile_external(
    #     self, profile_data: dict[str, Union[str, dict[str, str]]]
    # ) -> dict[str, Union[str, dict[str, str]]]:
    #     """
    #     Saves the profile information.
    #
    #     :param profile_data: The profile information to save.
    #     :return: The saved profile information.
    #     """
    #     return self._save_profile(profile_data=profile_data)

    def _load_profile(self) -> dict[str, Union[str, dict[str, str]]]:
        """
        Loads the profile information from local.

        :return: The loaded profile information.
        """
        # Load the data from the file
        try:
            with open(self._get_profile_path(), encoding="utf-8") as f:
                profile_data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Profile '{self.profile_id}' not found in '{self.profiles_path}'. Please scrape the profile first."
            )

        return profile_data

    def load_profile(self) -> dict[str, Union[str, dict[str, str]]]:
        """
        Loads the profile information from local.

        :return: The loaded profile information.
        """
        logger.info(f"Loading {self.profile_id} profile...")

        profile_data = self._load_profile()
        self.profile_data = profile_data

        logger.info("Loaded profile data.")
        logger.debug(f"Loaded {self.profile_id} profile : {profile_data}.")

        return profile_data

    def _clean_profile_slug(self, slug: str) -> str:
        """
        Cleans the profile slug.

        :param slug: The slug to clean.
        :return: The cleaned slug.
        """
        self.clean_profile_slug = slug

        return slug

    def _get_profile_slug(self) -> str:
        """
        Creates a slug for the profile.

        :return: The slug for the profile.
        """
        # Create the slug
        logger.info(f"Creating slug for {self.profile_id} profile...")
        slug = slugify(self.profile_id, separator="_")
        logger.debug(f"Created slug for {self.profile_id} profile : {slug}.")
        clean_slug = self._clean_profile_slug(slug)
        logger.info(f"Cleaned slug for {self.profile_id} profile : {clean_slug}.")

        return clean_slug

    def _get_profile_path(self) -> str:
        """
        Returns the path to the profile.

        :return: The path to the profile.
        """
        logger.info(f"Getting path for {self.profile_id} profile...")
        # Get the slug representing the profile name
        slug = self._get_profile_slug()

        # Get the service name
        service_name = self.service_name

        # Get the path to the profile
        path = os.path.join(self.profiles_path, f"{service_name}__{slug}.json")
        logger.debug(f"Got path for {self.profile_id} profile : {path}.")

        self.profile_path = path

        return path

    def download_profile(
        self,
        save_profile: bool = True,
        clean_profile: bool = True,
        force_scraping: bool = False,
    ) -> dict[str, Union[str, dict[str, str]]]:
        """
        Downloads a profile and returns the information as a dictionary.
        Profile is either scraped or loaded from local depending on the environment.
        Profile is either cleaned or not depending on the clean_profile parameter (default: True).

        :param save_profile: Whether to save the profile to a file or not
        :param clean_profile: Whether to clean the profile or not
        :param force_scraping: Whether to force the scraping using API or not
        :return: A dict containing the profile information.
        """
        logger.info(f"Downloading {self.profile_id} profile...")

        # Scrape the profile
        logger.info("Scraping profile...")
        profile_data = self.scrape_profile(force_scraping=force_scraping)

        # Clean the profile
        logger.info("Cleaning profile...")
        if clean_profile:
            profile_data_clean = self.clean_profile()
            self.profile_data = profile_data_clean
        else:
            profile_data_clean = profile_data

        # Save the profile
        logger.info("Saving profile...")
        if save_profile:
            self.save_profile()

        logger.info("Downloaded profile data.")

        return profile_data_clean
