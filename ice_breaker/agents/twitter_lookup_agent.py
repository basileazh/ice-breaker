from langchain.agents import AgentType, Tool, initialize_agent
from langchain.prompts.chat import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI

from ice_breaker.tools.tools import get_profile_url

# from ice_breaker.models.lookup_input import LookupInput


def lookup(profile_name: str) -> str:
    """
    Returns the Twitter profile username for a given name.

    :param profile_name: The name to lookup.
    :return: The Twitter profile username.
    """

    # Adding "Twitter" to the profile name to get better results
    profile_name = f"{profile_name} Twitter"

    # Define the prompt template
    template = """
    You are an expert in finding Twitter profiles from Google results.

    Given the full name {profile_name} I want you to find a link to their Twitter profile page,
     and extract from it their username.

    Your answer should contain only a Twitter username. remove everything that is not a username in your answer.
    only output the username and nothing else.
    """
    # If you have multiple options, choose the first one.
    chat_prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", template),
        ]
    )

    chat_prompt = chat_prompt_template.format_messages(profile_name=profile_name)

    # Define the tools for the agent
    tools = [
        Tool.from_function(
            func=get_profile_url,
            name="Crawl Google for Twitter username",
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing_errors=True,
            description="Useful for when you need to get the Twitter username for a given name.",
            # args_schema=LookupInput,
        ),
    ]

    # Define the LLM model for the agent
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    # Initialize the agent
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    twitter_username = agent.run(chat_prompt)

    return f"{twitter_username}"
