from langgraph.prebuilt import create_react_agent
from tools.extract_activity_information import extract_activity_information

interest_agent = create_react_agent(
    model="openai:gpt-4o",
    tools=[extract_activity_information],
    prompt=(
    """
    You are a travel interest extraction agent.

    Your job is to extract and maintain structured activity preferences from user input to support personalized itinerary planning
    by calling extract_activity_information tool.
    """
    ),
    name="interest_agent"
)
