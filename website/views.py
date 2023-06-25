from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from .forms import SignUpForm
from utils import book_collection, user_collection, Book, Person

# Create your views here.
def home(request):
    all_books = []
    try:
        db_books = list(book_collection.find())
        for book in db_books:
            one_book = Book(book["ID"], book["Name"], book["Description"], book["ISBN"], book["Page Count"],
                            book["Issued Out"], book["Author"], book["Year Published"])
            all_books.append(one_book)
    except:
        all_books = ["No Connection to Database Server", "Check your internet access"]
    return render(request, "home.html", {"books": all_books})

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

def testing(request):
  template = loader.get_template('template.html')
  context = {
    'fruits': ['Apple', 'Banana', 'Cherry'],   
  }
  return HttpResponse(template.render(context, request))