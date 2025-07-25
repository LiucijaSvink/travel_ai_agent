from langchain_core.tools import tool
from utils.utils import get_api_key
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from agents.schema import ItineraryResponse, DayPlan

tool_llm = ChatOpenAI(model="gpt-4o", temperature=0)

@tool
def generate_personalized_itinerary(
    destination: str = None,
    start_date: str = None,
    end_date: str = None,
    interests: str = None,
    avoids: str = None,
    transport: str = None
) -> dict:
    """
    Generate a personalized itinerary for a destination based on user preferences.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         """You are a travel assistant that creates fully personalized travel itineraries.

            Use the provided destination, travel dates, user interests, avoids, and transportation
            preferences to create a realistic and engaging day-by-day itinerary.

            Follow these detailed guidelines:

            Personalization:
            - Tailor the entire itinerary around the user's specific interests. For example, if
            they mention "nature, art, and no crowds", the plan should prioritize scenic walks,
            museums, and peaceful areas.
            - Respect all avoid preferences (e.g., crowded areas, tourist traps, nightlife) and
            exclude them completely.
            - Adapt to their preferred transportation:
            - For walking or bike, focus on neighborhoods and attractions close together.
            - For public transport or car, include more distant locations if worthwhile — but
                keep the routing logical and minimize backtracking.

            Use specific, real places:
            - Always refer to specific named places — museums, parks, cafés, neighborhoods,
            landmarks — instead of generic terms.
            - Avoid vague phrasing like “visit a local café” or “explore a museum.”
            - Instead, say: “Have lunch at Café de Flore”, “Visit the Musée d'Orsay”, or “Explore
            the Montmartre district.”
            - Ensure all places are realistic and located in the specified destination.

            Itinerary structure:
            - The itinerary should cover every day from start_date to end_date (inclusive).
            - If the dates are missing or the trip is longer than 7 days, default to a 3-day itinerary.
            - Each day must include:
            - `day`: e.g., "Day 1"
            - `description`: A natural and engaging summary (1–2 sentences), using time cues like:
                - “Start your morning…”, “In the afternoon…”, “After dinner…”

            Tone and output:
            - Use a natural, friendly tone. Write in second-person ("you").
            - Do not include assistant-style comments (e.g., “As your assistant…” or “I hope you enjoy…”).
            - Do not return shortened or incomplete responses unless explicitly instructed.
            - Return only the structured itinerary object, no commentary or wrapping text.

            Your goal is to deliver a realistic, well-paced, and highly personalized plan that feels like a
            local’s curated guide, not a generic tourist brochure.
            """),
        ("human",
         "Destination: {destination}\nDates: {start_date} to {end_date}\nInterests: {interests}\n"
         "Avoids: {avoids}\nPreferred Transport: {transport}")
    ])

    chain = prompt | tool_llm.with_structured_output(ItineraryResponse)
    result = chain.invoke({
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "interests": interests,
        "avoids": avoids,
        "transport": transport,
    })

    return result