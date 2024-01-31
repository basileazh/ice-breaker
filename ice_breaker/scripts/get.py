import json
from typing import Optional

import click

from ice_breaker.get_ice_breaker import get_ice_breaker


@click.command()
@click.argument("name_search", type=str)
@click.option(
    "-l",
    "--linkedin_profile_json",
    type=str,
    default=None,
    help="A path to an already existing LinkedIn profile JSON file. ",
)
@click.option(
    "-t",
    "--twitter_profile_json",
    type=str,
    default=None,
    help="A path to an already existing Twitter profile JSON file. ",
)
def get(name_search: str, linkedin_profile_json: Optional[str] = None, twitter_profile_json: Optional[str] = None) -> str:
    """
    Get the ice-breaker for a given name.
    It takes a name and some few distinctive elements, and returns the complete profile and an ice-breaker.

    :param name_search: Name for the Twitter and LinkedIn profiles to be found. Other elements may be added to it,
    for instance the current company or past school.
    :param linkedin_profile_json:  A path to an already existing LinkedIn profile JSON file.
    :param twitter_profile_json:  A path to an already existing Twitter profile JSON file.
    :return:  An ice-breaker for the associated name
    """
    # Load the LinkedIn profile JSON file if provided
    if linkedin_profile_json:
        with open(linkedin_profile_json) as f:
            linkedin_profile_data = json.load(f)
    else:
        linkedin_profile_data = None

    # Load the Twitter profile JSON file if provided
    if twitter_profile_json:
        with open(twitter_profile_json) as f:
            twitter_profile_data = json.load(f)
    else:
        twitter_profile_data = None

    # Get the ice-breaker
    ice_breaker = get_ice_breaker(
        name_search=name_search,
        linkedin_profile_data=linkedin_profile_data,
        twitter_profile_data=twitter_profile_data,
    )

    return ice_breaker
