import json
import os

from ice_breaker.core.log import logger
from ice_breaker.core.settings import DIR
from ice_breaker.get_profile import get_profile


def test_get_profile_linkedin():
    """
    Test the get_profile function for LinkedIn profiles.
    """
    # ## LinkedIn profile ## #

    # Get the LinkedIn profile URL for a given name
    linkedin_profile_url = "https://www.linkedin.com/in/yann-lecun/"
    logger.info(f"LinkedIn profile URL: {linkedin_profile_url}")

    # Scrape the LinkedIn profile
    linkedin_profile_data = get_profile(
        service_name="linkedin",
        profile_id=linkedin_profile_url,
        folder_path=None,
        clean_profile=True,
        save_profile=False,
        force_scraping=False,
    )

    # ## Assertions ## #

    # Check the profile data
    # load the LinkedIn profile JSON file from the data_samples folder
    with open(os.path.join(DIR, "tests/data/linkedin_sample_profile.json"), encoding="utf-8") as f:
        linkedin_profile_data_sample = json.load(f)

    assert linkedin_profile_data["full_name"] == linkedin_profile_data_sample["full_name"]
    assert linkedin_profile_data["headline"] == linkedin_profile_data_sample["headline"]
    assert linkedin_profile_data["summary"] == linkedin_profile_data_sample["summary"]
    assert linkedin_profile_data["experiences"] == linkedin_profile_data_sample["experiences"]
    assert linkedin_profile_data["education"] == linkedin_profile_data_sample["education"]
