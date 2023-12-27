from typing import Optional

import click

from ice_breaker.core.log import logger
from ice_breaker.core.settings import get_settings
from ice_breaker.services.service import get_service_class, get_services_list

ENVIRONMENT = get_settings("environment")


@click.command()
@click.argument("service_name", type=click.Choice(get_services_list()))
@click.argument("profile_id", type=str)
@click.option(
    "-p",
    "--folder_path",
    type=str,
    default=None,
    help="The complete path to the profiles' folder. If not provided, the profile will be saved in the data_samples folder.",
)
@click.option("--clean-profile/--no-clean-profile", is_flag=True, default=True, help="Whether to clean the profile or not.")
@click.option("--save-profile/--no-save-profile", is_flag=True, default=True, help="Whether to save the profile or not.")
@click.option("--force-scraping/--no-force-scraping", is_flag=True, default=False, help="Whether to save the profile or not.")
def download_profile(
    service_name: str,
    profile_id: str,
    folder_path: Optional[str] = None,
    clean_profile: bool = True,
    save_profile: bool = True,
    force_scraping: bool = False,
) -> None:
    """
    Downloads a LinkedIn or Twitter profile and saves the information as a dictionary.

    Please provide as arguments :
    - the service name (either "linkedin" or "twitter")
    - the account id (either a LinkedIn profile URL or a Twitter username)

    :param service_name: The service to use to download the profile.
    :param profile_id: The account id of the profile to download.
    :param folder_path: The complete path to the profile. Takes precedence over --filename argument. If not provided,
    the profile will be saved in the data_samples folder using the filename.
    :param clean_profile: Whether to clean the profile or not.
    :param save_profile: Whether to save the profile or not.
    :param force_scraping: Whether to force scraping the profile or allow loading from the disk.
    :return: None
    """
    logger.info(f"Downloading {service_name} {profile_id} profile...")

    logger.info("Service setting up...")
    # Service set up
    service = get_service_class(service_name)(
        profile_id=profile_id,
        environment=ENVIRONMENT,
        profiles_path=folder_path,
    )
    logger.info(f"Service set up : {service}.")

    logger.info(f"{service.service_name} {profile_id} profile downloading...")
    # Download the profile from the service
    profile = service.download_profile(
        clean_profile=clean_profile,
        save_profile=save_profile,
        force_scraping=force_scraping,
    )
    logger.info("Profile downloaded successfully.")

    logger.info(f"{service.service_name} {profile_id} profile downloaded : {profile}.")
    logger.info(f"{service.service_name} {profile_id} profile downloaded to {service.profile_path}.")
