from typing import Optional, Union
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate

from ice_breaker.agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from ice_breaker.agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from ice_breaker.services.linkedin_service import LinkedInService
from ice_breaker.services.twitter_service import TwitterService
from ice_breaker.core.log import logger
from ice_breaker.core.settings import get_settings

load_dotenv()
ENVIRONMENT = get_settings("environment")

def get_ice_breaker(
        name_search: str = "basile el azhari ekimetrics",
        linkedin_profile_data: Optional[dict[str, Union[str, dict[str, str]]]] = None,
        twitter_profile_data: Optional[dict[str, Union[str, dict[str, str]]]] = None,
):
    """
    This is the main function of the whole package.
    It takes a name and some few distinctive elements, and returns the complete profile and an ice-breaker.

    :param name_search: Name for the Twitter and LinkedIn profiles to be found. Other elements may be added to it,
    for instance the current company or past school.
    :param linkedin_profile_data: If provided, this LinkedIn profile will be used and the scraping will not be performed
    for LinkedIn
    :param twitter_profile_data: If provided, this Twitter profile will be used and the scraping will not be performed
    for Twitter
    :return: An ice-breaker for the associated name
    """
    # ## LinkedIn profile ## #

    if not linkedin_profile_data:
        # Get the LinkedIn profile URL for a given name
        linkedin_profile_url = linkedin_lookup_agent(profile_name=name_search)
        logger.info(f"LinkedIn profile URL: {linkedin_profile_url}")

        # Scrape the LinkedIn profile
        linkedin_service = LinkedInService(
            profile_id=linkedin_profile_url,
            environment=ENVIRONMENT,
        )
        linkedin_profile_data = linkedin_service.scrape_profile()

    # ## Twitter profile ## #

    if not twitter_profile_data:
        # Get the Twitter username for a given name
        twitter_username = twitter_lookup_agent(profile_name=name_search)
        logger.info(f"Twitter username: {twitter_username}")

        # Scraping Twitter data for a given username
        twitter_profile_data = TwitterService(
            profile_id=twitter_username,
            environment=ENVIRONMENT,
        )
        logger.info(f"Twitter data: {twitter_profile_data}")

    # ## Generate the ice-breaker ## #

    # Define the prompt template
    summary_template = """
    Given the LinkedIn information {linkedin_profile_data}
    and Twitter information {twitter_profile_data}
    about a person from I want you to create :
        1. a short summary
        2. two interesting facts about them
    """
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", summary_template),
        ]
    )

    chat_prompt.format_messages(
        linkedin_profile_data=linkedin_profile_data,
        twitter_profile_data=twitter_profile_data
    )

    # Define the LLM model
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.9)

    chain = chat_prompt | llm

    # Run the chain
    # TODO : change this "information" parameter
    res = chain.invoke({"information": linkedin_profile_data})

    logger.info(res.content)

    return res.content
