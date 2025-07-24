from langchain_core.tools import tool
import requests
from urllib.parse import urlencode, quote_plus

def build_booking_url(
    destination: str,
    start_date: str,
    end_date: str,
    adults: int = 2,
    rooms: int = 1,
    base_url: str = "https://www.booking.com/searchresults.html",
) -> str:
    """
    Constructs a Booking.com search URL based on the given parameters.
    """
    params = {
        "ss": destination,
        "checkin": start_date,
        "checkout": end_date,
        "group_adults": adults,
        "no_rooms": rooms,
        "order": "bayesian_review_score",
    }
    return f"{base_url}?{urlencode(params, quote_via=quote_plus)}"

def build_airbnb_url(
    destination: str,
    start_date: str,
    end_date: str,
    adults: int = 2,
    base_url: str = "https://www.airbnb.com/s/",
) -> str:
    """
    Constructs an Airbnb search URL for homes with superhosts in the given destination and dates.
    """
    params = {
        "checkin": start_date,
        "checkout": end_date,
        "adults": adults,
        "superhost": "true",
    }
    dest_encoded = quote_plus(destination)
    return f"{base_url}{dest_encoded}/homes?{urlencode(params)}"

def is_url_reachable(url: str, timeout: int = 5) -> bool:
    """
    Checks if the given URL is reachable via an HTTP HEAD request within the timeout.
    """
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException:
        return False

@tool
def search_accommodation(
    destination: str,
    start_date: str,
    end_date: str,
    adults: int = 2,
    rooms: int = 1,
) -> dict:
    """
    Returns reachable accommodation URLs from Booking.com and Airbnb for the given destination and dates.
    """
    results = {}

    booking_url = build_booking_url(destination, start_date, end_date, adults, rooms)
    if is_url_reachable(booking_url):
        results["booking"] = booking_url

    airbnb_url = build_airbnb_url(destination, start_date, end_date, adults)
    if is_url_reachable(airbnb_url):
        results["airbnb"] = airbnb_url

    return results