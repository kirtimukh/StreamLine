import certifi, dotenv, os, pymongo
import certifi
from openai import OpenAI

dotenv.load_dotenv()

openaiclient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
mongoclient = pymongo.MongoClient(
    os.getenv("MONGO_URI"),
    tlsCAFile=certifi.where(),
)
db = mongoclient.sample_mflix
collection = db.movies


def generate_embedding(text: str) -> list[float]:
    response = openaiclient.embeddings.create(
        input=text, model="text-embedding-ada-002"
    )
    return response.data[0].embedding


c = 0
for doc in collection.find({"plot": {"$exists": True}}):
    doc["embedding"] = generate_embedding(doc["plot"])
    collection.replace_one({"_id": doc["_id"]}, doc)

    c += 1

    if c % 50 == 0:
        print(f"Processed {c} documents")
