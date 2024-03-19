from functions import (
    get_current_weather,
    check_flight_details,
    make_me_coffee,
    search_movies,
)

available_functions = {
    "get_current_weather": {
        "function": get_current_weather,
        "args": ["location", "unit"],
    },
    "check_flight_details": {
        "function": check_flight_details,
        "args": ["departure_id", "arrival_id", "outbound_date", "return_date"],
    },
    "make_me_coffee": {
        "function": make_me_coffee,
        "args": [],
    },
    "search_movies": {
        "function": search_movies,
        "args": ["movie_description"],
    },
}


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_flight_details",
            "description": "Search flight availability and prices",
            "parameters": {
                "type": "object",
                "properties": {
                    "departure_id": {
                        "type": "string",
                        "description": "The code of the departure airport, e.g. SFO",
                    },
                    "arrival_id": {
                        "type": "string",
                        "description": "The code of the arrival airport, e.g. SFO",
                    },
                    "outbound_date": {
                        "type": "string",
                        "description": "Day of departure, e.g. 2022-12-31",
                    },
                    "return date": {
                        "type": "string",
                        "description": "Day of return, e.g. 2023-01-01",
                    },
                },
                "required": ["departure_id", "arrival_id", "outbound_date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "make_me_coffee",
            "description": "Asks a bot to make a cup of coffee with latte art",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_movies",
            "description": "Search for movies based on a description",
            "parameters": {
                "type": "object",
                "properties": {
                    "movie_description": {
                        "type": "string",
                        "description": "A description of the searched movie",
                    }
                },
                "required": ["movie_description"],
            },
        },
    },
]
