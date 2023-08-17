import pymongo, os
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from datetime import datetime, timedelta
from website.custom_storage import MediaStorage

load_dotenv()

uri = os.getenv("MONGODB_URI")

client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
database = client["LMS"]
book_collection = database["dBooks"]
user_collection = database["Users"]
borrowed_collection = database["BorrowedBooks"]
book_requests_collection = database["Book_Requests"]

def delete_image(file_path):
    """Delete Previous Image from storage"""

    # instantiate storage class to use
    prev_img = MediaStorage()
    
    # check functions before usage
    if prev_img.exists(file_path):
        prev_img.delete(file_path)

def handle_uploaded_image(image):
    """Upload image to storage S3 bucket"""
    # Set file directory you want to save files to
    file_directory_in_bucket = "media/book_images"

    # Synthesize (create) full file path, including filename
    file_path_in_bucket = os.path.join(file_directory_in_bucket, image.name)

    # Instantiate bucket
    media_storage = MediaStorage()

    media_storage.save(file_path_in_bucket, image)
    image_url = media_storage.url(file_path_in_bucket)

    # For development purposes only
    # with open("media/book_images/" + image.name, "wb+") as destination:
    #     for chunk in image.chunks():
    #         destination.write(chunk)
    return image_url, file_path_in_bucket

def edit_image_in_bucket(file_path, book_id):

    """Function to edit the name of file inside an S3 bucket"""
    media_storage = MediaStorage()

    # Check to ensure image exists
    if media_storage.exists(file_path):
        # Get the file object
        the_image = media_storage.open(file_path, mode='rb')
        slash = file_path.rfind("/")

        # determine the directory of file
        directory = file_path[:slash]

        # Change name of file
        curr_image = file_path[slash+1:]
        image_dot = curr_image.rfind(".")
        image_ext = curr_image[image_dot:]
        new_image = book_id + image_ext

        # Create file path with new name and save new image with new file_path
        new_file_path = os.path.join(directory, new_image)
        media_storage.save(new_file_path, the_image)

        image_url = media_storage.url(new_file_path)

        return image_url, new_file_path


def change_image_name(image, book_id):
    image_dot = str(image.name).rfind(".")
    
    # Include the dot, and give the whole extension
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


# dbx = dropbox.Dropbox(os.getenv("DROPBOX_ACCESS_TOKEN"))

# user = dbx.users_get_current_account()
# for entry in dbx.files_list_folder("").entries:
#     print(entry.name)

