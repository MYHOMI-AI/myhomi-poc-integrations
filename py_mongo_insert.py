sample_properties = [
    {
        "title": "3BHK Apartment in Jayanagar 2nd Block",
        "type": "apartment",
        "bhk": 3,
        "location": "Jayanagar 2nd Block",
        "price": 9500000,
        "area_sqft": 1400,
        "amenities": ["parking", "lift", "gym"]
    },
    {
        "title": "2BHK Apartment in JP Nagar",
        "type": "apartment",
        "bhk": 2,
        "location": "JP Nagar",
        "price": 7200000,
        "area_sqft": 1100,
        "amenities": ["parking", "lift"]
    },
    {
        "title": "4BHK Villa in Jayanagar 4th Block",
        "type": "villa",
        "bhk": 4,
        "location": "Jayanagar 4th Block",
        "price": 18500000,
        "area_sqft": 2500,
        "amenities": ["parking", "garden", "private terrace"]
    },
    {
        "title": "1BHK Studio in Koramangala",
        "type": "studio",
        "bhk": 1,
        "location": "Koramangala 6th Block",
        "price": 5200000,
        "area_sqft": 650,
        "amenities": ["parking", "lift"]
    },
    {
        "title": "3BHK Apartment near Indiranagar Metro",
        "type": "apartment",
        "bhk": 3,
        "location": "Indiranagar",
        "price": 10500000,
        "area_sqft": 1600,
        "amenities": ["gym", "clubhouse", "parking"]
    },
    {
        "title": "2BHK Flat in Jayanagar 2nd Block",
        "type": "apartment",
        "bhk": 2,
        "location": "Jayanagar 2nd Block",
        "price": 8300000,
        "area_sqft": 1200,
        "amenities": ["lift", "parking"]
    },
    {
        "title": "3BHK Duplex in BTM Layout",
        "type": "duplex",
        "bhk": 3,
        "location": "BTM Layout 1st Stage",
        "price": 9800000,
        "area_sqft": 1550,
        "amenities": ["parking", "balcony"]
    },
    {
        "title": "3BHK Apartment in Jayanagar 3rd Block",
        "type": "apartment",
        "bhk": 3,
        "location": "Jayanagar 3rd Block",
        "price": 9100000,
        "area_sqft": 1350,
        "amenities": ["lift", "gym"]
    }
]

from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
# Load environment variables from .env file

# MongoDB connection
# Ensure you have the following environment variables set in your .env file:
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

collection.insert_many(sample_properties)
print("Sample property data inserted.")
