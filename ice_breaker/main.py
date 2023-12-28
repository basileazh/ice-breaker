from dotenv import load_dotenv

from ice_breaker.agents.linkedin_lookup_agent import lookup as lookup_linkedin_agent

# from ice_breaker.agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from ice_breaker.core.log import logger
from ice_breaker.core.settings import get_settings
from ice_breaker.services.linkedin_service import LinkedInService

load_dotenv()
ENVIRONMENT = get_settings("environment")


name = "basile el azhari"


if __name__ == "__main__":
    logger.info("Hello, Langchain!")

    # ## LinkedIn lookup agent ## #

    # Get the LinkedIn profile URL for a given name
    linkedin_profile_url = lookup_linkedin_agent(profile_name=name)
    logger.info(f"LinkedIn profile URL: {linkedin_profile_url}")

    # Scrape the LinkedIn profile
    linkedin_service = LinkedInService(
        profile_id=linkedin_profile_url,
        environment=ENVIRONMENT,
    )
    linkedin_profile_data = linkedin_service.scrape_profile()

    # ## Twitter lookup agent ## #

    # # Get the Twitter username for a given name
    # twitter_username = twitter_lookup_agent(profile_name=name)
    # logger.info(f"Twitter username: {twitter_username}")
    #
    # # Scraping Twitter data for a given username
    # twitter_data = scrape_twitter_profile(username=twitter_username)
    # logger.info(f"Twitter data: {twitter_data}")

    # # Define the prompt template
    # summary_template = """
    # Given the LinkedIn information {information} about a person from I want you to create :
    #     1. a short summary
    #     2. two interesting facts about them
    # """
    # chat_prompt = ChatPromptTemplate.from_messages(
    #     [
    #         ("system", summary_template),
    #     ]
    # )
    #
    # # chat_prompt.format_messages(information=information)
    # # Define the LLM model
    # llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.9)
    #
    # chain = chat_prompt | llm
    #
    # # Run the chain
    # res = chain.invoke({"information": linkedin_profile_data})
    #
    # logger.info(res.content)
