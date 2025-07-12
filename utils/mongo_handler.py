from pymongo import MongoClient
import pandas as pd
from pathlib import Path
import os
import pymongo

# Constants
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "doctor_app"
COLLECTION_NAME = "availability_data"
CSV_FILE_PATH = Path("data/doctor_availability.csv")

# Mongo client
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def load_from_mongo():
    """
    Fetch the data from MongoDB and save it to a local CSV file.
    """
    print("📥 Loading data from MongoDB...")
    records = list(collection.find({}, {"_id": 0}))
    if not records:
        print("⚠️ No data found in MongoDB.")
        return
    df = pd.DataFrame(records)
    CSV_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)  # ensure 'data/' exists
    df.to_csv(CSV_FILE_PATH, index=False)
    print("✅ Data loaded from MongoDB and saved locally.")


def load_to_mongo():
    """
    Read the local CSV file and upload it to MongoDB.
    """
    print("📤 Saving data to MongoDB...")
    if not CSV_FILE_PATH.exists():
        print("❌ CSV file not found at:", CSV_FILE_PATH)
        return
    df = pd.read_csv(CSV_FILE_PATH)
    collection.delete_many({})  # optional: wipe old data
    collection.insert_many(df.to_dict(orient="records"))
    print("✅ Local CSV data saved to MongoDB.")
