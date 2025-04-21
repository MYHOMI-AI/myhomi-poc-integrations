import openai
from openai import OpenAI
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
AIclient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/", username=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
db = client["real_estate"]
collection = db["properties"]

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

def ask_openai_about_properties(prompt, property_info):
    full_prompt = f"""You are a helpful assistant that only answers based on property listings provided below.

Property Listings:
{property_info}

User Query:
{prompt}

Respond with helpful information strictly based on the listings."""

    response = AIclient.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    user_prompt = input("What kind of property are you looking for?\n> ")
    docs = get_matching_properties(user_prompt)
    context = format_properties(docs)
    print("\n--- Matching Listings ---\n", context)

    if docs:
        response = ask_openai_about_properties(user_prompt, context)
        print("\n--- GPT Response ---\n", response)
