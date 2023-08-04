import pymongo, os
from pymongo.server_api import ServerApi
from django.core.files.storage import FileSystemStorage
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGODB_URI")

client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
database = client["LMS"]
book_collection = database["dBooks"]
user_collection = database["Users"]
request_return_collection = database["Request_Return"]
requests_collection = database["Book_Requests"]

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


# first = book_collection.create_index([("ID", pymongo.ASCENDING)], unique=True)

# human = Person("vickerdent", "Victor", "Abuka", "vickerdent@gmail.com", "No. 42, Winners' Way, Dawaki, Abuja", "F.C.T.", True, True)

# first = user_collection.insert_one(human.to_dict())

# create this when opportune
# what = book_collection.create_index([("Slug", pymongo.ASCENDING)], unique=True)
# print(what)