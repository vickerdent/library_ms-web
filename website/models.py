from django.db import models
from django.utils.text import slugify

def correct_id(name) -> str:
    """ Used to Introduce correct
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

# Create your models here.
class BookModel(models.Model):
    """Create model for the Book class"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    isbn = models.CharField()
    page_count = models.IntegerField()
    issued_out = models.BooleanField(default=False)
    author = models.CharField()
    year = models.CharField(max_length=4)
    image = models.ImageField(upload_to="book_images/"+ correct_id(name))
    quantity = models.IntegerField(default=0)
    series = models.BooleanField(default=False)
    name_of_series = models.CharField(blank=True)
    pos_in_series = models.IntegerField(blank=True)
    genre = models.TextField()
    
    

class RequestBook(models.Model):
    """Create model for requesting books """
    name = models.CharField(max_length=100)
    author = models.CharField()

from datetime import datetime

class Book:
    def __init__(self, book_id: str, name: str, description: str, isbn: str, page_count: int,
                 issued_out: bool, author: str, year: str, quantity: int=0,
                 series: bool=False, name_of_series: str="", pos_in_series: int=None,
                 genre: list=[], image: str="", slug=None, issuee: list=[]):
        self.book_id = book_id
        self.name = name
        self.description = description
        self.isbn = isbn
        self.page_count = page_count
        self.issued_out = issued_out
        self.author = author
        self.year = year
        self.issuee = issuee
        self.image = image
        self.quantity = quantity
        self.slug = slug
        self.series = series
        self.name_of_series = name_of_series
        self.pos_in_series = pos_in_series
        self.genre = genre

    def to_dict(self) -> dict:
        """ Converts the class's details into a dictionary """
        diction = {}
        if self.slug == None:
            diction = {
                "ID": self.book_id, 
                "Name": self.name,
                "Description": self.description,
                "ISBN": self.isbn, 
                "Page Count": self.page_count,
                "Issued Out": self.issued_out,
                "Author": self.author,
                "Year Published": self.year,
                "Book Image": self.image,
                "Quantity": self.quantity,
                "Genre": self.genre,
                "Slug": slugify(self.name),
                "Part Of A Series": self.series,
                "Name Of Series": self.name_of_series,
                "Position In Series": self.pos_in_series,
                }
        else:
            diction = {
                "ID": self.book_id, 
                "Name": self.name,
                "Description": self.description,
                "ISBN": self.isbn, 
                "Page Count": self.page_count,
                "Issued Out": self.issued_out,
                "Author": self.author,
                "Year Published": self.year,
                "Book Image": self.image,
                "Quantity": self.quantity,
                "Genre": self.genre,
                "Slug": self.slug,
                "Part Of A Series": self.series,
                "Name Of Series": self.name_of_series,
                "Position In Series": self.pos_in_series,
                }
        return diction
    
    def __str__(self) -> str:
        return self.name
    
    def no_image(self) -> dict:
        """ Converts the class's details into a dictionary without an image"""
        diction = {}
        if self.slug == None:
            diction = {
                "ID": self.book_id, 
                "Name": self.name,
                "Description": self.description,
                "ISBN": self.isbn, 
                "Page Count": self.page_count,
                "Issued Out": self.issued_out,
                "Author": self.author,
                "Year Published": self.year,
                "Quantity": self.quantity,
                "Genre": self.genre,
                "Slug": slugify(self.name),
                "Part Of A Series": self.series,
                "Name Of Series": self.name_of_series,
                "Position In Series": self.pos_in_series,
                }
        else:
            diction = {
                "ID": self.book_id, 
                "Name": self.name,
                "Description": self.description,
                "ISBN": self.isbn, 
                "Page Count": self.page_count,
                "Issued Out": self.issued_out,
                "Author": self.author,
                "Year Published": self.year,
                "Quantity": self.quantity,
                "Genre": self.genre,
                "Slug": self.slug,
                "Part Of A Series": self.series,
                "Name Of Series": self.name_of_series,
                "Position In Series": self.pos_in_series,
                }
        return diction
    
    def hide_id(self) -> dict:
        """To abstract book.id from other functions"""
        book_dictionary = {
            "Name": self.name,
            "Description": self.description,
            "ISBN": self.isbn, 
            "Page Count": self.page_count,
            "Issued": self.issued_out,
            "Author": self.author,
            "Year Published": self.year
        }
        return book_dictionary

class RequestABook:
    """Create class for requesting books """
    def __init__(self, name: str, author: str) -> None:
        self.name = name
        self.author = author

    def to_dict(self) -> dict:
        """Creates a dictionary for updating MongoDB"""
        diction = {
            "Name": self.name,
            "Author": self.author
        }
        return diction


class Request_Return_Info:
    """Class to handle the requesting and
        returning of books to and from the web application"""
    def __init__(self, book_id: str, username: str, action: str, post_date=datetime.now) -> None:
        self.book_id = book_id
        self.username = username
        self.action = action
        self.post_date = post_date

    def to_dict(self) -> dict:
        """ Converts the class's info into a dictionary """
        diction = {
            "Book ID": self.book_id,
            "Username": self.username,
            "Action": self.action, # Borrow / Return
            "Post Date": self.post_date,
        }
        return diction
    
class Person:
    """Class handling the definition of who a person is
        to the web application"""
    def __init__(self, username: str, first_name: str, last_name: str, email: str, 
                 address: str, state: str, is_admin=False, is_staff=False):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.state = state
        self.is_admin = is_admin
        self.is_staff = is_staff

    def to_dict(self) -> dict:
        """ Converts the class's into a dictionary """
        diction = {
            "First Name": self.first_name,
            "Last Name": self.last_name,
            "Username": self.username,
            "Email": self.email,
            "Address": self.address,
            "State": self.state,
            "Is Admin": self.is_admin,
            "Is Staff": self.is_staff
        }
        return diction