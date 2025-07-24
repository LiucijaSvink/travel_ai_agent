from langchain_core.tools import tool
from utils.utils import get_api_key
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from agents.schema import ActivityPreferences

tool_llm = ChatOpenAI(model="gpt-4o", temperature=0)

@tool
def extract_activity_information(input: str) -> dict:
    """
    Extract structured activity preferences (interests, avoids, transport) from user input text.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         """You are an assistant that extracts structured travel preferences from user input.
        Return a JSON object with three fields:
        - 'interests': what activities or experiences the user is interested in
        - 'avoids': what they want to avoid
        - 'transport': preferred mode of transportation

        Only return the JSON object. If any fields are missing from the user input, set their values to null.
        """),
        ("human", "{input}")
    ])

    chain = prompt | tool_llm.with_structured_output(ActivityPreferences)

    result = chain.invoke({"input": input})
    return result