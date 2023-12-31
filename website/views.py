from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.text import slugify

from .forms import SignUpForm, EditBookForm, BookForm, BorrowBookForm, RequestABookForm, \
    EditImageForm, ConfirmCodeForm
from utils import book_collection, user_collection, pymongo, reg_accounts_collection, \
    book_requests_collection, borrowed_collection, return_status, send_email_code
from .o_functions import change_image_name, calculate_return, correct_id
from .custom_storage import handle_uploaded_image, delete_image, edit_image_in_bucket
from .models import Book, Person, RequestABook, BorrowedBook, BorrowedBookInstance
from datetime import datetime

# Create your views here.
def home(request):
    return_status()
    all_books = []
    try:
        db_books = list(book_collection.find().sort("Name", pymongo.ASCENDING))
        for book in db_books:
            if request.user.is_authenticated:
                if request.user.email not in book["Issuees"]:
                    one_book = Book(book["ID"], book["Name"], book["Description"], book["ISBN"],
                                    book["Page Count"], book["Issued Out"], book["Author"],
                                    book["Year Published"], book["Quantity"], book["Part Of A Series"],
                                    book["Name Of Series"], book["Position In Series"], book["Genre"],
                                    book["Book Image"], book["Slug"], book["Issuees"])
                    all_books.append(one_book)
            else:
                one_book = Book(book["ID"], book["Name"], book["Description"], book["ISBN"],
                                    book["Page Count"], book["Issued Out"], book["Author"],
                                    book["Year Published"], book["Quantity"], book["Part Of A Series"],
                                    book["Name Of Series"], book["Position In Series"], book["Genre"],
                                    book["Book Image"], book["Slug"], book["Issuees"])
                all_books.append(one_book)
    except:
        all_books = ["No Connection to Database Server", "Try again in a short while."]

    if request.user.is_authenticated:
        #check if user is confirmed and is staff from MongoDB
        user = user_collection.find_one({"Email": request.user.email, "registered": True})
        if not user:
            return redirect("confirm_code")
        elif user and user["Is Staff"] == True:
            return render(request, "home.html", {"books": all_books, "staff": True})

    return render(request, "home.html", {"books": all_books, "staff": False})

def search(request):
    all_books = []
    search_term = request.GET["search_term"]
    lookup_books = list(book_collection.aggregate([
        {"$search": {
            "index": "default",
            "text": {
                "query": search_term,
                "path": {
                    "wildcard": "*"
                }
            }
        }}
    ]))

    for book in lookup_books:
        if request.user.is_authenticated:
            if request.user.email not in book["Issuees"]:
                one_book = Book(book["ID"], book["Name"], book["Description"], book["ISBN"],
                                book["Page Count"], book["Issued Out"], book["Author"],
                                book["Year Published"], book["Quantity"], book["Part Of A Series"],
                                book["Name Of Series"], book["Position In Series"], book["Genre"],
                                book["Book Image"], book["Slug"], book["Issuees"])
                all_books.append(one_book)
        else:
            one_book = Book(book["ID"], book["Name"], book["Description"], book["ISBN"],
                                book["Page Count"], book["Issued Out"], book["Author"],
                                book["Year Published"], book["Quantity"], book["Part Of A Series"],
                                book["Name Of Series"], book["Position In Series"], book["Genre"],
                                book["Book Image"], book["Slug"], book["Issuees"])
            all_books.append(one_book)

    if request.user.is_authenticated:
        #check if user is confirmed and is staff from MongoDB
        user = user_collection.find_one({"Email": request.user.email})
        if user and user["Is Staff"] == True:
            return render(request, "search.html", {"books": all_books, "staff": True, "search": search_term})
        
    return render(request, "search.html", {"books": all_books, "staff": False, "search": search_term})

def login_user(request):
    # check if login attempt or normal request
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "You have logged in successfully.")
            return redirect("home")
        else:
            messages.error(request, "Incorrect username or password.")
            return redirect("login")
    return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, "You've been logged out successfully.")
    return redirect("home")

def sign_up(request):
    # check if registration attempt or normal request
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email") # get email from form
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists! Email must be unique!")
                return render(request, "signup.html", {"form": form})

            # Add user to MongoDB
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            address = form.cleaned_data.get("address")
            state = form.cleaned_data.get("state")

            new_user = Person(username, first_name, last_name, email, address, state)

            user_collection.insert_one(new_user.to_dict())

            form.save()
            # Send Confirmation code to user
            send_email_code(email)
            
            # Authenticate and login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have signed up and logged in successfully.")
            return redirect("confirm_code")
    else:
        form = SignUpForm()
        return render(request, "signup.html", {"form": form})

def book_details(request, book):
    return_status()
    # Look up record for book
    book = book_collection.find_one({"Slug": book})
    if book:
        # note that images is saved using book.id, not slug
        current_book = Book(book["ID"], book["Name"], book["Description"], book["ISBN"],
                            book["Page Count"], book["Issued Out"], book["Author"],
                            book["Year Published"], book["Quantity"], book["Part Of A Series"],
                            book["Name Of Series"], book["Position In Series"], book["Genre"],
                            book["Book Image"], book["Slug"], book["Issuees"])

        if request.user.is_authenticated:
            #check if user is staff from MongoDB
            user = user_collection.find_one({"Email": request.user.email})

            if user and user["Is Staff"] == True:
                return render(request, "book.html", {"book": current_book, "staff": True})
            
        return render(request, "book.html", {"book": current_book, "staff": False})
    else:
        messages.error(request, "Book does not exist!")
        return render(request, "404.html", {})

def borrow(request, book):
    # Check that user is logged in
    if request.user.is_authenticated:
        book = book_collection.find_one({"Slug": book})
        
        if book:
            # check to ensure user has not already borrowed book
            if request.user.email in book["Issuees"]:
                messages.error(request, "Book already borrowed!")
                return redirect("home")
        
            current_book = Book(book["ID"], book["Name"], book["Description"], book["ISBN"],
                            book["Page Count"], book["Issued Out"], book["Author"],
                            book["Year Published"], book["Quantity"], book["Part Of A Series"],
                            book["Name Of Series"], book["Position In Series"], book["Genre"],
                            book["Book Image"], book["Slug"], book["Issuees"])
            form = BorrowBookForm(request.POST or None)
            if form.is_valid():
                email = request.user.email
                book_id = current_book.book_id
                return_date = calculate_return(form.cleaned_data["duration"])

                new_borrow = BorrowedBook(email, book_id, return_date, return_date)
                borrowed_collection.insert_one(new_borrow.to_dict())
                book_collection.update_one({"ID": book_id}, {
                    "$addToSet": {"Issuees": email}
                })
                messages.success(request, "You have borrowed a new book!")
                return redirect("home")
            return render(request, "borrow.html", {"book": current_book, "form": form})
        else:
            messages.error(request, "Book does not exist!")
            return render(request, "404.html", {})
    else:
        messages.info(request, "You must be logged in to borrow a book")
        return redirect("login")

def add_book(request, dname=None, dauthor=None):
    if request.user.is_authenticated:
        #check if user is staff from MongoDB
        user = user_collection.find_one({"Email": request.user.email})

        # if name and author are given pass initial
        if dname and dauthor:
            initial = {"name": dname, "author": dauthor}
        else:
            initial = None

        if user is not None and user["Is Staff"] == True:
            form = BookForm(request.POST or None, request.FILES or None, initial=initial)
            if form.is_valid():
                name = form.cleaned_data["name"]
                book_id = correct_id(name)
                description = form.cleaned_data["description"]
                isbn = form.cleaned_data["isbn"]
                page_count = form.cleaned_data["page_count"]
                issued_out = False
                author = form.cleaned_data["author"]
                year = form.cleaned_data["year"]
                quantity = form.cleaned_data["quantity"]
                series = False
                name_of_series = form.cleaned_data["name_of_series"]
                pos_in_series = form.cleaned_data["pos_in_series"]
                genre = form.cleaned_data["genre"]
                image = request.FILES["image"]
                
                old_book = book_collection.find_one({"ID": book_id})
                if old_book is not None:
                    book_id += str(len(list(book_collection.find({"Slug": old_book["Slug"]}, {"ID": 1}))) + 1)

                image.name = change_image_name(image, book_id)

                image_url, image_path = handle_uploaded_image(image)

                new_genre = str(genre).split(", ")
                if form.cleaned_data["series"] == "True":
                    series = True

                new_book = Book(book_id, name, description, isbn, page_count, issued_out, author,
                                year, quantity, series, name_of_series, pos_in_series, 
                                new_genre, [image_url, image_path])
                
                book_collection.insert_one(new_book.to_dict())
                if initial and dname and dauthor:
                    book_requests_collection.delete_one({"name": dname, "author": dauthor})

                messages.success(request, "You have successfully added a book.")
                return redirect("book", book = slugify(new_book.name))
            
            return render(request, "add_book.html", {"form": form, "staff": True})
        else:
            messages.info(request, "You are not a staff! Kindly submit this form to \
                          get a book added to the library")
            return redirect("request_book")
    else:
        messages.info(request, "You must be logged in to add a book")
        return redirect("login")

def edit_book(request, book):
    if request.user.is_authenticated:
        #check if user is staff from MongoDB
        user = user_collection.find_one({"Email": request.user.email})

        if user is not None and user["Is Staff"] == True:
            # proceed if user is a staff member
            current_book = book_collection.find_one({"Slug": book})
            # change quantity as soon as changes are saved
            if current_book is not None:
                #current_book exists in database: mongoDB
                #introduce has changed after adding images for current current_book
                d_genre = current_book["Genre"]
                holder = d_genre[0]
                for item in d_genre:
                    if item == d_genre[0]:
                        continue
                    holder += ", " + item

                curr_series = "False"
                curr_issued_out = "False"

                if current_book["Issued Out"] == True:
                    curr_issued_out = "True"
                
                if current_book["Part Of A Series"] == True:
                    curr_series = "True"

                # Define initial data from mongodb that should be preloaded
                initial = {"book_id": current_book["ID"], "name": current_book["Name"], "description": current_book["Description"], 
                        "isbn": current_book["ISBN"], "page_count": current_book["Page Count"], "issued_out": curr_issued_out,
                        "author": current_book["Author"], "year": current_book["Year Published"],
                        "quantity": current_book["Quantity"], "genre": holder, "series": curr_series,
                        "name_of_series": current_book["Name Of Series"], "pos_in_series": current_book["Position In Series"]}
                
                # proceed if user (a staff member) submitted the form and current_book exists
                form = EditBookForm(request.POST or None, initial=initial)
                if form.is_valid():
                    # obtain data from form
                    name = form.cleaned_data["name"]
                    # obtain new id from edited book's name, whether name changed or not
                    book_id = correct_id(name)
                    description = form.cleaned_data["description"]
                    isbn = form.cleaned_data["isbn"]
                    page_count = form.cleaned_data["page_count"]
                    issued_out = False
                    author = form.cleaned_data["author"]
                    year = form.cleaned_data["year"]
                    quantity = form.cleaned_data["quantity"]
                    series = False
                    name_of_series = form.cleaned_data["name_of_series"]
                    pos_in_series = form.cleaned_data["pos_in_series"]
                    genre = form.cleaned_data["genre"]
                    # image = request.FILES["image"]

                    if form.cleaned_data["issued_out"] == "True":
                        issued_out = True

                    if form.cleaned_data["series"] == "True":
                        series = True

                    new_slug = current_book["Slug"]

                    if book_id == current_book["ID"]:

                        new_genre = str(genre).split(", ")

                        changed_book = Book(book_id, name, description, isbn, page_count, 
                                            issued_out, author, year, quantity,
                                            series, name_of_series, pos_in_series, new_genre)
                        book_collection.update_one({"ID": book_id}, {
                            "$set": changed_book.no_image()
                        })
                    else:
                        # check if new book's id already exists
                        neo_book = book_collection.find_one({"ID": book_id})
                        if neo_book is not None:
                            # if different book (neo_book) exists, add a number to edited book id
                            book_id += str(len(list(book_collection.find({"Slug": current_book["Slug"]}, {"ID": 1}))) + 1)

                            new_genre = str(genre).split(",")
                            # also add a number to slug for book
                            new_slug += str(len(list(book_collection.find({"Slug": current_book["Slug"]}, {"ID": 1}))) + 1)
                            
                            # Edit book image in file storage to equate book_id
                            # Check parameters if change is needed, else you're done for
                            # Note that function can return None
                            image_url, image_path = edit_image_in_bucket(current_book["Image"][1], book_id)

                            new_book = Book(book_id, name, description, isbn, page_count, issued_out,
                                            author, year, quantity, series, name_of_series, pos_in_series, 
                                            new_genre, [image_url, image_path], new_slug, current_book["Issuees"])
                            book_collection.insert_one(new_book.to_dict())
                            book_collection.delete_one({"ID": current_book["ID"]})
                        else:
                            new_genre = str(genre).split(",")
                            
                            #Handle image storage in S3 bucket 
                            image_url, image_path = edit_image_in_bucket(current_book["Image"][1], book_id)

                            new_book = Book(book_id, name, description, isbn, page_count,
                                            issued_out, author, year, quantity, series,
                                            name_of_series, pos_in_series, new_genre,
                                            [image_url, image_path], None, current_book["Issuees"])
                            book_collection.insert_one(new_book.to_dict())
                            book_collection.delete_one({"ID": current_book["ID"]})

                            messages.success(request, "You have successfully updated the book.")
                            return redirect("book", book = slugify(new_book.name))
                    
                    messages.success(request, "You have successfully updated the book.")
                    return redirect("book", book = new_slug)
                return render(request, "edit_book.html", {"form": form, "staff": True})
            else:
                #book does not exist. Get out of here
                messages.info(request, "Book does not exist. Add book to database.")
                return redirect("add_book")
        else:
            messages.info(request, "You are not a staff! Reach out to a staff for help on this issue.")
            return redirect("home")
    else:
        messages.error(request, "You must be logged in to view that page...")
        return redirect("login")
    
def edit_book_image(request, book):
    if request.user.is_authenticated:
        #check if user is staff from MongoDB
        user = user_collection.find_one({"Email": request.user.email})

        if user and user["Is Staff"] == True:
            curr_book = book_collection.find_one({"Slug": book})
            if curr_book is not None:
                #current_book exists in database: mongoDB
                form = EditImageForm(request.POST or None, request.FILES or None)
                if form.is_valid():
                    image = request.FILES["image"]
                    delete_image(curr_book["Book Image"][1])

                    # Adjust uploaded image's name to fit book's ID
                    image.name = change_image_name(image, curr_book["ID"])
                    image_url, image_path = handle_uploaded_image(image)

                    book_collection.update_one({"ID": curr_book["ID"]}, {
                        "$set": {"Book Image": [image_url, image_path]}
                    })

                    messages.success(request, "You have successfully updated the book.")
                    return redirect("book", book = curr_book["Slug"])
                
                return render(request, "edit_book_image.html", {"form": form, "staff": True})
            else:
                #book does not exist. Get out of here
                messages.info(request, "Book does not exist. Add book to database.")
                return redirect("add_book")
        else:
            messages.info(request, "You are not a staff! Reach out to a staff for help on this issue.")
            return redirect("home")
    else:
        messages.error(request, "You must be logged in to view that page!")
        return redirect("login")

def delete_book(request, book):
    if request.user.is_authenticated:
        #check if user is staff from MongoDB
        user = user_collection.find_one({"Email": request.user.email})

        if user is not None and user["Is Staff"] == True:
            curr_book = book_collection.find_one({"Slug": book})
            if curr_book is not None:
                delete_image(curr_book["Book Image"][1])

            book_collection.delete_one({"Slug": book})
            messages.success(request, "You have successfully deleted the book.")
            return redirect("home")
        else:
            messages.info(request, "You are not a staff! Reach out to a staff for help on this issue.")
            return redirect("home")
    else:
        messages.info(request, "You must be logged in to delete a book!")
        return redirect("login")
    
def delete_request(request, dname, dauthor):
    if request.user.is_authenticated:
        #check if user is staff from MongoDB
        user = user_collection.find_one({"Email": request.user.email})

        if user is not None and user["Is Staff"] == True:
            book_requests_collection.delete_one({"name": dname, "author": dauthor})

            messages.success(request, "You have successfully deleted the request.")
            return redirect("requested_books")
        else:
            messages.info(request, "You are not a staff! Reach out to a staff for help on this issue.")
            return redirect("home")
    else:
        messages.info(request, "You must be logged in to delete a request!")
        return redirect("login")

def request_book(request):
    form = RequestABookForm(request.POST or None)
    if form.is_valid():
        new_request = RequestABook(form.cleaned_data["name"], form.cleaned_data["author"])
        for book in list(book_collection.find()):
            if str(book["Name"]).lower() == new_request.name.lower():
                messages.info(request, "Book already exists!")
                return render(request, "request_book.html", {"form": form})
            
        for book in list(book_requests_collection.find()):
            if str(book["name"]).lower() == new_request.name.lower():
                messages.info(request, "Book already requested and in process!")
                return render(request, "request_book.html", {"form": form})
            
        book_requests_collection.insert_one(new_request.to_dict())
        messages.success(request, "You have successfully requested the book.")
        return redirect("home")
    return render(request, "request_book.html", {"form": form})

def history(request):
    return_status()
    if request.user.is_authenticated:
        super_list = []
        for item in list(borrowed_collection.find({"email": request.user.email})):
            book = book_collection.find_one({"ID": item["book_id"]})
            if book:
                book = BorrowedBookInstance(book["Name"], str(item["date_borrowed"].day) + "/"
                                             + str(item["date_borrowed"].month) + "/" + 
                                             str(item["date_borrowed"].year), str(item["return_date"].day)
                                             + "/" + str(item["return_date"].month) + "/" + 
                                             str(item["return_date"].year), str(item["expected_return"].day)
                                             + "/" + str(item["expected_return"].month) + "/" + 
                                             str(item["expected_return"].year),
                                             item["returned"], book["Slug"])
                super_list.append(book)
        return render(request, "history.html", {"books": super_list})
    else:
        messages.info(request, "You must be logged in to view this page!")
        return redirect("login")

def return_book(request):
    # on return, delete the borrower's username from the
    # book's issuee's list, and change issued out to false
    if request.user.is_authenticated:
        super_list = []
        for item in list(borrowed_collection.find({"email": request.user.email, "returned": False})):
            book = book_collection.find_one({"ID": item["book_id"]})
            if book:
                super_list.append({"name": book["Name"], "slug": book["Slug"]})
        return render(request, "return_book.html", {"books": super_list})
    else:
        messages.info(request, "You must be logged in to view borrowed books!")
        return redirect("login")


def process_return(request, book):
    # check that user is logged in
    if request.user.is_authenticated:
        curr_book = book_collection.find_one({"Slug": book})
        if curr_book:
            # return borrowed book by updtaing concerned collections
            book_collection.update_one({"Slug": book},
                                   {"$pull": {"Issuees": request.user.email}})
            borrowed_collection.update_one({"book_id": curr_book["ID"]},
                                           {"$set": {"returned": True, "return_date": datetime.now()}})
            messages.success(request, "You have successfully returned the book.")
            return redirect("home")
        else:
            messages.error(request, "Book does not exist!")
            return render(request, "404.html", {})
    else:
        messages.info(request, "You must be logged in to return a book!")
        return redirect("login")
    
def requested_books(request):
    # check that user is logged in
    if request.user.is_authenticated:
        #check if user is staff from MongoDB
        user = user_collection.find_one({"Email": request.user.email})

        if user and user["Is Staff"] == True:
            # proceed if user is a staff member
            all_books = list(book_requests_collection.find())

            return render(request, "requested_books.html", {"books": all_books,"staff": True})
        else:
            messages.info(request, "You are not a staff! Reach out to a staff for help on this issue.")
            return redirect("home")
    else:
        messages.info(request, "You must be logged in view this page!")
        return redirect("login")
        
def confirm_code(request):
    # check that user is logged in
    if request.user.is_authenticated:
        if user_collection.find_one({"Email": request.user.email, "registered": True}):
            messages.info(request, "Account is already confirmed.")
            return redirect("home")
        
        form = ConfirmCodeForm(request.POST or None)
        if form.is_valid():
            code = form.cleaned_data["code"]
            new_user = reg_accounts_collection.find_one({"email": request.user.email})
            if new_user and code == new_user["passcode"]:
                user_collection.update_one({"Email": request.user.email}, 
                                           {"$set": {"registered": True}})
                return redirect("home")
            else:
                messages.error(request, "Confirmation code is incorrect!")
                return render(request, "confirm_code.html", {"form": form})
        return render(request, "confirm_code.html", {"form": form})
    else:
        messages.info(request, "You must be logged in view this page!")
        return redirect("login")
    
def resend_code(request):
    # check that user is logged in
    if request.user.is_authenticated:
        if user_collection.find_one({"Email": request.user.email, "registered": True}):
            messages.info(request, "Account is already confirmed.")
            return redirect("home")
        reg_accounts_collection.delete_one({"email": request.user.email})
        send_email_code(request.user.email)
        return redirect("confirm_code")
    else:
        messages.info(request, "You must be logged in to do this!")
        return redirect("login")

def staff(request):
    # check that user is logged in
    if request.user.is_authenticated:
        #check if user is staff from MongoDB
        user = user_collection.find_one({"Email": request.user.email})

        if user and user["Is Staff"] == True:
            # proceed if user is a staff member

            non_staff = []
            all_staff = []
            
            not_staff = list(user_collection.find({"Is Staff": False}))
            a_staff = list(user_collection.find({"Is Staff": True}))

            for staff in a_staff:
                all_staff.append(Person(staff["Username"], staff["First Name"], staff["Last Name"], staff["Email"],
                                        staff["Address"], staff["State"], staff["registered"], staff["Is Admin"],
                                        staff["Is Staff"]))
            
            for staff in not_staff:
                non_staff.append(Person(staff["Username"], staff["First Name"], staff["Last Name"], staff["Email"],
                                        staff["Address"], staff["State"], staff["registered"], staff["Is Admin"],
                                        staff["Is Staff"]))

            return render(request, "staff.html", {"non_staff": non_staff, "all_staff": all_staff, "staff": True})
        else:
            messages.info(request, "You are not a staff! Reach out to a staff for help on this issue.")
            return redirect("home")
    else:
        messages.info(request, "You must be logged in view this page!")
        return redirect("login")
    
def add_staff(request, username):
    if request.user.is_authenticated:
        #check if user is staff from MongoDB

        user = user_collection.find_one({"Email": request.user.email})
        if user and user["Is Staff"] == True:
            # proceed if user is a staff member

            mold = user_collection.find_one({"Username": username})
            if mold and not mold["Is Staff"]:
                user_collection.update_one(
                    {"Username": username},
                    {"$set": {"Is Staff": True}}
                )
                messages.info(request, "User has been added to staff successfully!")
                return redirect("staff")
            else:
                messages.info(request, "User does not exist!")
                return redirect("staff")
        else:
            messages.info(request, "You are not a staff! Reach out to a staff for help on this issue.")
            return redirect("home")
    else:
        messages.info(request, "You must be logged in view this page!")
        return redirect("login")
    
def remove_staff(request, username):
    if request.user.is_authenticated:
        #check if user is staff from MongoDB

        user = user_collection.find_one({"Email": request.user.email})
        if user and user["Is Staff"] == True:
            # proceed if user is a staff member

            mold = user_collection.find_one({"Username": username})
            if mold and mold["Is Staff"]:
                user_collection.update_one(
                    {"Username": username},
                    {"$set": {"Is Staff": False}}
                )
                messages.info(request, "User has been removed from staff successfully!")
                return redirect("staff")
            else:
                messages.info(request, "User does not exist!")
                return redirect("staff")
        else:
            messages.info(request, "You are not a staff! Reach out to a staff for help on this issue.")
            return redirect("home")
    else:
        messages.info(request, "You must be logged in view this page!")
        return redirect("login")

def privacy_policy(request):
    return render(request, "privacy.html", {})