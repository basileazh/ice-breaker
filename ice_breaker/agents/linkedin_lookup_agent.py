from langchain.agents import AgentType, Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate

from ice_breaker.tools.tools import get_profile_url

# from ice_breaker.models.lookup_input import LookupInput


def lookup(profile_name: str) -> str:
    """
    Returns the LinkedIn profile URL for a given name.

    :param profile_name: The name to lookup.
    :return: The LinkedIn profile URL.
    """

    # Define the prompt template
    template = """
    You are an expert in finding LinkedIn profiles from Google results.

    Given the full name {profile_name} I want you to find the LinkedIn URL for them.

    examples of linkedin profile urls:
    https://fr.linkedin.com/in/firstname-lastname-123456789/
    https://fr.linkedin.com/in/john-doe/
    https://uk.linkedin.com/in/jbgette/
    https://ca.linkedin.com/in/jack-hill/
    https://fr.linkedin.com/in/basile-el-azhari/

    Your answer should contain only a URL. remove everything that is not a url in your answer.
    only output the url and nothing else.
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
            name="Crawl Google for LinkedIn URL",
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing_errors=True,
            description="Useful for when you need to get the LinkedIn profile URL for a given name.",
            # args_schema=LookupInput,
        ),
    ]

    # Define the LLM model for the agent
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    # Initialize the agent
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    linkedin_profile_url = agent.run(chat_prompt)

    return f"{linkedin_profile_url}"
