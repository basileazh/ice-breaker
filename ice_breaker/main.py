from dotenv import load_dotenv

from ice_breaker.agents.linkedin_lookup_agent import lookup as lookup_linkedin_agent
from ice_breaker.services.linkedin import scrape_linkedin_profile

load_dotenv()


if __name__ == "__main__":
    print("Hello, Langchain!")

    # Get the LinkedIn profile URL for a given name
    linkedin_profile_url = lookup_linkedin_agent(profile_name="jean-baptiste gette")

    # Scrape the LinkedIn profile
    linkedin_profile_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)

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
    # print(res.content)
