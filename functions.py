import os, json, pymongo, certifi
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


aiclient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
mongoclient = pymongo.MongoClient(
    os.getenv("MONGO_URI"),
    tlsCAFile=certifi.where(),
)


def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    elif "san francisco" in location.lower():
        return json.dumps(
            {"location": "San Francisco", "temperature": "72", "unit": unit}
        )
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})


def check_flight_details(departure_id, arrival_id, outbound_date, return_date=None):
    print(
        departure_id,
        arrival_id,
        outbound_date,
        return_date,
    )
    from serpapi import GoogleSearch

    params = {
        "engine": "google_flights",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "return_date": return_date,
        "currency": "USD",
        "hl": "en",
        "api_key": "09e45465e3a374e435d71ab61f8592af70b4b489ba91ea170cd2cebc5b7b4f52",
        "type": 2,
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    depa = results["best_flights"][0]["flights"][0]["departure_airport"]["name"]
    arra = results["best_flights"][0]["flights"][0]["arrival_airport"]["name"]

    dets = []

    for det in results["best_flights"]:
        flight_det = det["flights"][0]
        dets.append(
            {
                "departure_time": flight_det["departure_airport"]["time"],
                "arrival_time": flight_det["arrival_airport"]["time"],
                "duration": flight_det["duration"],
                "airplane": flight_det["airplane"],
                "airline": flight_det["airline"],
                "flight_number": flight_det["flight_number"],
            }
        )

    return json.dumps(
        {
            "departure_airport": depa,
            "arrival_airport": arra,
            "flights": dets,
        }
    )


def make_me_coffee():
    import random

    latte_art = [
        "heart",
        "tulip",
        "swan",
        "phoenix",
    ]
    return json.dumps(
        {
            "coffee_maker": "Mochabot",
            "estimated_time": "5 minutes",
            "status": "brewing",
            "message": "I'm brewing your coffee! 🤖☕️",
            "latte_art": random.choice(latte_art),
        }
    )


def generate_embedding(text):
    response = aiclient.embeddings.create(input=text, model="text-embedding-ada-002")
    return response.data[0].embedding


def search_movies(movie_description):

    db = mongoclient.sample_mflix
    collection = db.movies
    results = collection.aggregate(
        [
            {
                "$vectorSearch": {
                    "queryVector": generate_embedding(movie_description),
                    "path": "embedding",
                    "numCandidates": 20,
                    "limit": 4,
                    "index": "plot_index",
                }
            }
        ]
    )

    suggestions = []
    for document in results:
        suggestions.append(
            {
                "title": document["title"],
                "plot": document["plot"],
            }
        )
    return json.dumps(suggestions)
