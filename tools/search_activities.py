from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from agents.schema import ActivityItem, ActivityList

tool_llm = ChatOpenAI(model="gpt-4o", temperature=0)

@tool
def search_activities(destination: str) -> dict:
    """
    Search for top recommended tourist activities in a destination.
    Returns a JSON dict with a list of activities.
    """
    query = (
        f"What are the top tourist attractions, activities, or unique experiences in {destination}?"
        f"Return relevant travel articles or content."
    )

    tavily = TavilySearch(max_results=5, include_answer=True)
    response = tavily.invoke({"query": query})

    combined_context = "\n\n".join([r["content"] for r in response["results"] if "content" in r])

    prompt = ChatPromptTemplate.from_messages([
        ("system", 
        f"""You are a travel activity planner.
        Given content from travel websites, extract up to 5 top recommended activities for tourists in {destination}.
        Return a JSON object with a list of activities under a field named 'activities'. Each activity must include:

        - name
        - description (3 sentences max)
        - location (specific place or area)
        - recommended_duration (e.g., "1-2 hours", "Half-day", etc.)
        - activity_link (if no specific link is found, use a general link from the source)

        Think step by step and only include high-quality, diverse activities.
        """),
        ("human", "{context}")
    ])

    chain = prompt | tool_llm.with_structured_output(ActivityList)
    result = chain.invoke({"context": combined_context})

    return result.model_dump()