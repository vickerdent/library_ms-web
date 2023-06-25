import pymongo
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from entities import Book, Person

load_dotenv()
import os

uri = os.getenv("MONGODB_URI")

client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
database = client["LMS"]
book_collection = database["dBooks"]
user_collection = database["Users"]

# first = book_collection.create_index([("ID", pymongo.ASCENDING)], unique=True)

# human = Person("Victor", "Abuka", "vickerdent@gmail.com", "No. 42, Winners' Way, Dawaki, Abuja", "F.C.T.")

# first = user_collection.insert_one(human.to_dict())

# created
# what = user_collection.create_index([("Email", pymongo.ASCENDING)], unique=True)
