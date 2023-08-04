from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.files.images import ImageFile
from django.utils.text import slugify
from .forms import SignUpForm, EditBookForm, BookForm, RequestBookForm
from utils import book_collection, user_collection, pymongo, \
    requests_collection, handle_uploaded_image, delete_image, change_image_name
from .models import Book, Person, correct_id, RequestABook

# Create your views here.
def home(request):
    all_books = []
    try:
        db_books = list(book_collection.find().sort("Name", pymongo.ASCENDING))
        for book in db_books:
            one_book = Book(book["ID"], book["Name"], book["Description"], book["ISBN"],
                            book["Page Count"], book["Issued Out"], book["Author"],
                            book["Year Published"], book["Quantity"], False, "", None, [], None, book["Slug"])
            all_books.append(one_book)
    except:
        all_books = ["No Connection to Database Server", "Try again in a short while."]

    if request.user.is_authenticated:
        #check if user is staff from MongoDB
        user = user_collection.find_one({"Email": request.user.email})
        if user is not None and user["Is Staff"] == True:
            return render(request, "home.html", {"books": all_books, "staff": True})

    return render(request, "home.html", {"books": all_books, "staff": False})

def login_user(request):
    # check if login attempt or normal request
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
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
                return redirect("register")
            form.save()

            # Add user to MongoDB
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            address = form.cleaned_data.get("address")
            state = form.cleaned_data.get("state")

            new_user = Person(username, first_name, last_name, email, address, state)

            user_collection.insert_one(new_user.to_dict())

            # Authenticate and login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have signed up and logged in successfully.")
            return redirect("home")
    else:
        form = SignUpForm()
        return render(request, "signup.html", {"form": form})
    
    return render(request, "signup.html", {"form": form})

def book_details(request, slug):
    # Look up record for book
    book = book_collection.find_one({"Slug": slug})
    if book is not None:
        # note that images is saved using book.id, not slug
        current_book = Book(book["ID"], book["Name"], book["Description"], book["ISBN"],
                            book["Page Count"], book["Issued Out"], book["Author"],
                            book["Year Published"], book["Quantity"], book["Part Of A Series"],
                            book["Name Of Series"], book["Position In Series"], book["Genre"],
                            book["Book Image"], book["Slug"])

        if request.user.is_authenticated:
            #check if user is staff from MongoDB
            user = user_collection.find_one({"Email": request.user.email})

            if user is not None and user["Is Staff"] == True:
                return render(request, "book.html", {"book": current_book, "staff": True})
            
        return render(request, "book.html", {"book": current_book, "staff": False})
    else:
        messages.error(request, "Book does not exist!")
        return render(request, "404.html", {})

def borrow(request, slug):
    # on return, delete the borrower's username from the
    # book's issuee's list, and change issued out to false
    if request.user.is_authenticated:
        return render(request, "borrow.html", {})
    else:
        messages.info(request, "You must be logged in to borrow a book")
        return redirect("login")

def add_book(request):    
    if request.user.is_authenticated:
        #check if user is staff from MongoDB
        user = user_collection.find_one({"Email": request.user.email})

        if user is not None and user["Is Staff"] == True:
            form = BookForm(request.POST or None, request.FILES or None)
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

                handle_uploaded_image(image)

                new_genre = str(genre).split(", ")
                if form.cleaned_data["series"] == "True":
                    series = True

                new_book = Book(book_id, name, description, isbn, page_count, issued_out, author,
                                year, quantity, series, name_of_series, pos_in_series, 
                                new_genre, image.name)
                
                book_collection.insert_one(new_book.to_dict())

                messages.success(request, "You have successfully added a book.")
                return redirect("book", slug = slugify(new_book.name))
            
            return render(request, "add_book.html", {"form": form, "staff": True})
        else:
            messages.info(request, "You are not a staff! Kindly submit this form to \
                          get a book added to the library")
            return redirect("request_book")
    else:
        messages.info(request, "You must be logged in to add a book")
        return redirect("login")

def edit_book(request, slug):
    if request.user.is_authenticated:
        #check if user is staff from MongoDB
        user = user_collection.find_one({"Email": request.user.email})

        if user is not None and user["Is Staff"] == True:
            # proceed if user is a staff member
            current_book = book_collection.find_one({"Slug": slug})
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
                        # book name never changed, then proceed like so:
                        # delete_image(current_book["Book Image"])
                            
                        # book_id is the same as unedited book in mongodb
                        # image.name = change_image_name(image, book_id)

                        # MAKE SURE TO DELETE PREVIOUS IMAGE (if book image was changed)
                        # handle_uploaded_image(image)

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
                            # image.name = change_image_name(image, book_id)

                            # MAKE SURE TO DELETE PREVIOUS IMAGE (if book image was changed)
                            # handle_uploaded_image(image)
                            # delete_image(current_book["Book Image"])

                            new_genre = str(genre).split(",")
                            # also add a number to slug for book
                            new_slug += str(len(list(book_collection.find({"Slug": current_book["Slug"]}, {"ID": 1}))) + 1)

                            new_book = Book(book_id, name, description, isbn, page_count,
                                            issued_out, author, year, quantity, series,
                                            name_of_series, pos_in_series, new_genre, new_slug)
                            book_collection.insert_one(new_book.to_dict())
                            book_collection.delete_one({"ID": current_book["ID"]})
                        else:
                            # image.name = change_image_name(image, book_id)

                            # MAKE SURE TO DELETE PREVIOUS IMAGE FIRST (if book image was changed)
                            # handle_uploaded_image(image)
                            # delete_image(current_book["Book Image"])

                            new_genre = str(genre).split(",")

                            new_book = Book(book_id, name, description, isbn, page_count,
                                            issued_out, author, year, quantity, series,
                                            name_of_series, pos_in_series, new_genre)
                            book_collection.insert_one(new_book.to_dict())
                            book_collection.delete_one({"ID": current_book["ID"]})

                            messages.success(request, "You have successfully updated the book.")
                            return redirect("book", slug = slugify(new_book.name))
                    
                    messages.success(request, "You have successfully updated the book.")
                    return redirect("book", slug = new_slug)
                return render(request, "edit_book.html", {"form": form})
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
    
def delete_book(request, slug):
    if request.user.is_authenticated:
        #check if user is staff from MongoDB
        user = user_collection.find_one({"Email": request.user.email})

        if user is not None and user["Is Staff"] == True:
            curr_book = book_collection.find_one({"Slug": slug})
            if curr_book is not None:
                delete_image(curr_book["Book Image"])

            book_collection.delete_one({"Slug": slug})
            messages.success(request, "You have successfully deleted the book.")
            return redirect("home")
        else:
            messages.info(request, "You are not a staff! Reach out to a staff for help on this issue.")
            return redirect("home")
    else:
        messages.info(request, "You must be logged in to delete a book!")
        return redirect("login")

def request_book(request):
    if request.method == "POST":
        form = RequestBookForm(request.POST)
        name = form.cleaned_data["name"]
        author = form.cleaned_data["author"]

        new_request = RequestABook(name, author)
        requests_collection.insert_one(new_request.to_dict())

    else:
        form = RequestBookForm()
    return render(request, "request_book.html", {"form": form})


