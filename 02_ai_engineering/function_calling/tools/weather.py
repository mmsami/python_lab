import urllib.error
import urllib.request
from urllib.parse import quote


def get_weather(city: str) -> str:
    encoded_city = quote(city)
    url = f"https://wttr.in/{encoded_city}?format=3"
    try:
        with urllib.request.urlopen(url=url, timeout=10) as response:
            data = response.read().decode("utf-8")
            return data.strip()
    except urllib.error.HTTPError as e:
        # Handle specific HTTP errors (404, 500, etc.)
        if e.code == 404:
            return f"City '{city}' not found."
        elif e.code == 500:
            return f"Server error for '{city}'. Please try again later."
        else:
            return f"HTTP error {e.code} for '{city}': {e.reason}"
    except urllib.error.URLError as e:
        # Network issues (DNS failure, connection refused, timeout)
        return f"Network error for '{city}': {e.reason}"
    except Exception as e:
        # Any other unexpected error
        return f"Unexpected error for '{city}': {e}"


SCHEMA = {
    "name": "get_weather",
    "description": "Get current wetaher for a city",
    "parameters": {
        "type": "object",
        "properties": {"city": {"type": "string", "description": "City name"}},
        "required": ["city"],
    },
}

if __name__ == "__main__":
    print(get_weather("London"))
    print(get_weather("New York"))
    print(get_weather("InvalidCityNameThatDoesNotExist"))
