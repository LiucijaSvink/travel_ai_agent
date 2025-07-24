from pydantic import BaseModel
from typing import Optional, Sequence, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated

class TravelPreferences(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class DayPlan(BaseModel):
    day: str
    description: str

class ItineraryResponse(BaseModel):
    itinerary: List[DayPlan]

class ActivityPreferences(BaseModel):
    interests: Optional[str] = None
    avoids: Optional[str] = None
    transport: Optional[str] = None

class ActivityItem(BaseModel):
    name: str
    description: str
    location: str
    recommended_duration: str
    activity_link: str

class ActivityList(BaseModel):
    activities: List[ActivityItem]