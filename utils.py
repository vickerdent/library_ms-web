import pymongo, os
from pymongo.server_api import ServerApi
from django.core.files.storage import FileSystemStorage
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

uri = os.getenv("MONGODB_URI")

client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
database = client["LMS"]
book_collection = database["dBooks"]
user_collection = database["Users"]
borrowed_collection = database["BorrowedBooks"]
book_requests_collection = database["Book_Requests"]

def delete_image(image_name):
    # Delete Previous Image
    # instantiate storage class to use
    prev_img = FileSystemStorage()
    if prev_img.exists("book_images/" + image_name):
        prev_img.delete("book_images/" + image_name)

def handle_uploaded_image(image):
    with open("media/book_images/" + image.name, "wb+") as destination:
        for chunk in image.chunks():
            destination.write(chunk)

def change_image_name(image, book_id):
    image_dot = str(image.name).rfind(".")
    image_ext = image.name[image_dot:]
    return str(book_id) + str(image_ext)

def correct_id(name) -> str:
    """ Used to introduce correct
        IDs for books"""
    the_index = 0
    new_input = str(name).strip()
    d_id = new_input[the_index]
    while the_index < len(new_input):
        if new_input[the_index] == ' ':
            the_index += 1
            d_id += new_input[the_index]
            continue
        the_index += 1
    return d_id


# first = book_collection.create_index([("ID", pymongo.ASCENDING)], unique=True)

# human = Person("vickerdent", "Victor", "Abuka", "vickerdent@gmail.com", "No. 42, Winners' Way, Dawaki, Abuja", "F.C.T.", True, True)

# first = user_collection.insert_one(human.to_dict())

# create this when opportune
# what = book_collection.create_index([("Slug", pymongo.ASCENDING)], unique=True)
# print(what)

# To make this much faster, you should probably create an aggregation pipeline
def return_status():
    today = datetime.now()
    for item in list(borrowed_collection.find()):
        if today + timedelta(days=0) >= item["expected_return"] and not item["returned"]:
            borrowed_collection.update_one({"_id": item["_id"]},
                                           {"$set": {"returned": True, "return_date": today}})
            book_collection.update_one({"ID": item["book_id"]},
                                       {"$pull": {"Issuees": item["email"]}})

def calculate_return(duration):
    """Calculate return date
    for borrowed book for a user"""
    today = datetime.now()
    return_date = today
    if duration == "1 Day":
        return_date = today + timedelta(days=1)
    elif duration == "3 Days":
        return_date = today + timedelta(days=3)
    elif duration == "1 Week":
        return_date = today + timedelta(weeks=1)
    elif duration == "3 Weeks":
        return_date = today + timedelta(weeks=3)
    return return_date