from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from datetime import datetime
from agents.schema import TravelPreferences

tool_llm = ChatOpenAI(model="gpt-4o", temperature=0)

@tool
def summarize_input(input: str) -> dict:
    """
    Extract origin, destination, start_date, end_date from user input as JSON dict.
    """
    current_date = datetime.now().date().isoformat()
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
        f"""You are an extractor and verifier of user input. Extract origin, destination, start_date and end_date from the input.

        Today is {current_date}.

        Extraction rules:
        - If the user provides only a city, infer the country as well (e.g., "Paris" → "Paris, France").
        - Verify that origin and destination are valid city or location names.
            - If invalid, set that specific field to None.
        - If origin or destination is obviously not a location (e.g., random words like 'apple'), set that field to None.
        - If end_date is earlier than start_date, set both to None.
        - If the start_date or end_date is in the past (before today's date {current_date}), treat it invalid and set to None.
        - If the user gives both a start_date and a duration (e.g., "5 days"), compute the end_date.
        - If only duration is given but no start_date, set both dates as None.
        - If only start_date is given, set end_date to None.
        - If the city name is misspelled but recognizable, correct it to the proper spelling.
        - If the user specifies a date without a year, assume they mean the next upcoming occurrence of that date. Use today's date ({current_date}) 
        to decide whether it's this year or next.
        - Accept common date formats like "2025-07-24" or "2025/07/24", and convert all to ISO 8601 (YYYY-MM-DD).
        - Do not discard valid fields even if others are invalid. Extract what you can.
        - Do not explain your reasoning or return anything else — just the JSON object."""
        ),
        ("human", "{user_input}")
    ])
    chain = prompt | tool_llm.with_structured_output(TravelPreferences)
    result = chain.invoke({"user_input": input})
    return result.model_dump()