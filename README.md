# AI-Powered Travel Planning Agent

This Streamlit app helps users plan their trips using an intelligent travel assistant powered by LLM agents and real-time tools. From extracting travel preferences expressed in natural language to suggesting flights, accommodations, and activities — this app reduces planning effort and saves time.

## Deployed Application

Try out the live version of the Travel Planning Agent here:  
[Travel Planning Agent - Live App](https://travelaiagent-qvsgksxgdshpzv7wkfimvl.streamlit.app/)

---

## Agent Purpose

The Travel Assistant is designed to support users during the early stages of trip planning. Instead of filling out forms, users can describe their plans in natural language — and the AI takes care of the rest.

---

## Key Capabilities

- Extracts structured preferences from user input:
  - Origin and Destination  
  - Start and End Dates  
  - Optional: interests, dislikes, preferred transportation mode
- Suggests accommodation links via Booking.com and Airbnb
- Recommends tourist attractions and popular activities
- Provides personalized activity recommendations based on user interests
- Answers general travel questions (e.g., visa requirements, packing tips)

> **Note:**  
> The search for the fastest direct flights via the Amadeus API is implemented but temporarily disabled due to an API disruption.  
> For more information, see: [Amadeus for Developers](https://developers.amadeus.com/)

---

## Architecture (LangGraph)

The application uses a LangGraph-based supervisor agent to orchestrate specialized sub-agents and tools.

### Agents

- `preference_agent`: Extracts and confirms core travel preferences
- `interest_agent`: Extracts user preferences related to activities (e.g., history, nightlife, nature)
- `action_agent`: Executes tools for accommodation search, popular attraction discovery, or personalized activity suggestions

### Subloops

- **Preference Collection Loop**  
  Repeats until all required travel preferences (origin, destination, dates) are extracted and confirmed.

- **Activity Preference Collection Loop**  
  Gathers and confirms user interests and dislikes before generating personalized activity recommendations.

- **Action Execution Loop**  
  Executes tools conditionally based on the user’s request (e.g., hotels, attractions, activities).

---
### Environment Setup

Your `.streamlit/secrets.toml` or local `.env` file should include:

```toml
OPENAI_API_KEY = "..."
TAVILY_API_KEY = "..."
LANGSMITH_API_KEY = "..."
```

LangSmith tracing (optional) is enabled with:

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_PROJECT"] = "AI_travel_planning_agent"

## Technical Design Decisions

- **LangGraph**: Orchestrates control flow with loops over missing preferences and conditional tool calls.

- **Conversation History as Memory**: All user messages, agent responses, and tool call outputs are stored as conversation history, which the agent uses for reference and context.

- **LLM Tool-Use**: The assistant selectively calls tools like `search_accommodation` or `search_activities` based on user requests.  
  *(Note: `search_fastest_flights` is currently disabled due to API issues.)*

- **LangSmith Tracing**: Enables transparent debugging and performance monitoring via LangSmith.

---

## Evaluation

The agent’s accuracy and responsiveness was assessed through user testing using the following common use cases:

| User Input                                                     | Agent Response                                                                                                                                                                                                                                  |
|----------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| I want to travel from Paris to London, starting on 2025-07-24 and returning by 2025-07-29. | Here are the details of your trip: Origin: Paris, Destination: London, Start Date: 2025-07-24, End Date: 2025-07-29. Would you like to search for accommodation, see top tourist attractions, or plan a personalized itinerary? You can also ask me anything else travel-related! |
| Search flights                                                | Fetches fastest direct flights (when API enabled)                                                                                                                                                                                             |
| Find me a hotel                                              | You can explore hotel options in London using the following links:<br>• [Booking.com](https://www.booking.com/searchresults.html?ss=London%2C+United+Kingdom&checkin=2025-07-24&checkout=2025-07-29&group_adults=2&no_rooms=1&order=bayesian_review_score)<br>• [Airbnb](https://www.airbnb.com/s/London%2C+United+Kingdom/homes?checkin=2025-07-24&checkout=2025-07-29&adults=2&superhost=true) |
| Search top tourist attractions                               | Here are some top tourist attractions in London:<br><br>**London Eye**<br>Description: The London Eye is a giant Ferris wheel on the South Bank of the River Thames. It offers breathtaking views of the city skyline and is a must-visit for first-time tourists. The experience is both thrilling and serene, providing a unique perspective of London. |
| Plan me a personalized itinerary please                      | Could you please share your activity preferences, such as what you enjoy doing while traveling, what you’d like to avoid, and your preferred means of transportation? This will help us tailor the itinerary to your liking.                    |
| I enjoy food and nature, dislike loud places and prefer to walk | Here is a personalized 5-day itinerary for your trip to London, based on your preferences of enjoying food and nature, avoiding loud places, and preferring to walk: <br><br>**Day 1:**<br>**Morning:** Explore Hyde Park: Walk through one of London’s largest and most famous parks, enjoying the natural beauty and peaceful atmosphere. |
| Update my travel preferences to: origin Vilnius, destination Rome | Here are the updated details of your trip: Origin: Vilnius, Destination: Rome, Start Date: 2025-07-24, End Date: 2025-07-29. Would you like to search for accommodation, explore top tourist attractions, or plan a personalized itinerary for Rome? Let me know how I can assist you further! |
| Update my interests: I like culture and art, avoid nature. Would like to travel everywhere by car. | Your travel preferences have been updated:<br>**Interests:** Culture and Art<br>**Avoids:** Nature<br>**Transportation preference:** Travel by car |
| I want to travel from moon to sun, starting on 2025-07-24 and returning by 2025-07-29. | Sorry, I couldn't understand your preferences. Could you please rephrase or provide clearer travel details? |
| I want to travel from Paris to London, starting on 2023-07-24 and returning by 2023-07-29. | Sorry, I couldn't understand your preferences. Could you please rephrase or provide clearer travel details? |

## Ethical Considerations

This application uses only legally licensed APIs and publicly available data sources to provide travel information. User privacy is respected by not storing or sharing personal data beyond the scope of the current session. The AI assistant is designed to support and augment user decision-making without replacing professional travel advice.

## Future Improvements

- **Scalability:** Migrate to a more scalable cloud infrastructure with auto-scaling capabilities to handle higher user demand seamlessly.
- **Flight Search API:** Re-enable and expand flight search functionality with additional providers for better coverage and pricing options.
