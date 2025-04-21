import openai
from openai import OpenAI
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
AIclient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# MongoDB setup
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_collection = os.getenv("DB_COLLECTION")
if db_port is None:
    db_port = 27017  # Default MongoDB port

if db_host is None:
    raise ValueError("DB_HOST environment variable is not set.")

if db_name is None:
    raise ValueError("DB_NAME environment variable is not set.")

if db_collection is None:
    raise ValueError("DB_COLLECTION environment variable is not set.")

client = MongoClient(f"mongodb://{db_host}:{db_port}/", username=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
db = client[db_name]
collection = db[db_collection]

def list_available_models():
    try:
        models = AIclient.models.list()
        available = [model.id for model in models.data]
        print("\n--- Available OpenAI Models ---")
        for m in available:
            print(f"- {m}")
        return available
    except Exception as e:
        print(f"Error fetching models: {e}")
        return []

def get_best_available_model():
    available = list_available_models()
    if "gpt-4" in available:
        return "gpt-4"
    elif "gpt-3.5-turbo" in available:
        return "gpt-3.5-turbo"
    else:
        raise RuntimeError("No suitable GPT model found in your OpenAI account.")

def parse_search_criteria(prompt):
    criteria = {}
    if "2bhk" in prompt.lower(): criteria["bhk"] = 2
    if "3bhk" in prompt.lower(): criteria["bhk"] = 3
    if "apartment" in prompt.lower(): criteria["type"] = "apartment"
    if "villa" in prompt.lower(): criteria["type"] = "villa"
    if "jayanagar" in prompt.lower(): criteria["location"] = {"$regex": "jayanagar", "$options": "i"}
    return criteria

def get_matching_properties(prompt):
    criteria = parse_search_criteria(prompt)
    return list(collection.find(criteria).limit(5))

def format_properties(docs):
    if not docs:
        return "No matching properties found."
    
    result = ""
    for doc in docs:
        result += (
            f"- {doc.get('title', 'Unnamed Property')}\n"
            f"  Type: {doc.get('type')}, BHK: {doc.get('bhk')}, Location: {doc.get('location')}\n"
            f"  Area: {doc.get('area_sqft')} sqft, Price: ₹{doc.get('price')}\n"
            f"  Amenities: {', '.join(doc.get('amenities', []))}\n\n"
        )
    return result.strip()

def ask_openai_about_properties(prompt, property_info, model_name):
    full_prompt = f"""You are a helpful assistant that only answers based on property listings provided below.

Property Listings:
{property_info}

User Query:
{prompt}

Respond with helpful information strictly based on the listings."""

    response = AIclient.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    model_name = get_best_available_model()
    
    user_prompt = input("\nWhat kind of property are you looking for?\n> ")
    docs = get_matching_properties(user_prompt)
    context = format_properties(docs)
    print("\n--- Matching Listings ---\n", context)

    if docs:
        response = ask_openai_about_properties(user_prompt, context, model_name)
        print("\n--- GPT Response ---\n", response)
