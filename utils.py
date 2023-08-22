import pymongo, os, ssl, smtplib
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from datetime import datetime, timedelta
from email.message import EmailMessage
from website.o_functions import code_generator

load_dotenv()

uri = os.getenv("MONGODB_URI")

client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
database = client["LMS"]
book_collection = database["dBooks"]
user_collection = database["Users"]
borrowed_collection = database["BorrowedBooks"]
book_requests_collection = database["Book_Requests"]
reg_accounts_collection = database["RegisteredAccounts"]

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

def send_email_code(receiver: str):
    email_sender = os.getenv("EMAIL_SENDER" )
    email_password = os.getenv("EMAIL_PASSWORD")
    code = code_generator()

    subject = "Confirm Your Account on Library_MS"
    body = f"""
        Here is your one-time passcode: {code}
        This code will expire in 59 minutes.



        Got any problem? Simply reply us
        """
    # Run Mongo_DB Code Here
    reg_accounts_collection.insert_one({"email": receiver, "passcode": code})

    msg = EmailMessage()
    msg["From"]  = email_sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, receiver, msg.as_string())
