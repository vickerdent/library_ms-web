from django.db import models
from django.utils.text import slugify
from datetime import datetime

# Create your models here.
from datetime import datetime

class Book:
    """Class for handling books to and
    from MongoDB within the application"""

    __slots__ = ("book_id", "name", "description", "isbn", "page_count", "issued_out", 
                 "author", "year", "issuees", "image", "quantity", "slug", "series",
                 "name_of_series", "pos_in_series", "genre")
    def __init__(self, book_id: str, name: str, description: str, isbn: str, page_count: int,
                 issued_out: bool, author: str, year: str, quantity: int=0,
                 series: bool=False, name_of_series: str="", pos_in_series: int=None,
                 genre: list=[], image: str="", slug=None, issuees: list=[]):
        self.book_id = book_id
        self.name = name
        self.description = description
        self.isbn = isbn
        self.page_count = page_count
        self.issued_out = issued_out
        self.author = author
        self.year = year
        self.issuees = issuees
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
                "Issuees": self.issuees
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
                "Issuees": self.issuees
                }
        return diction
    
    def __str__(self) -> str:
        return self.name
    
    def no_image(self) -> dict:
        """ Converts the class's details into a dictionary
        without an image nor issuees"""
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
    
    __slots__ = ("name", "author")

    def __init__(self, name: str, author: str) -> None:
        self.name = name
        self.author = author

    def to_dict(self) -> dict:
        """Creates a dictionary for updating MongoDB"""
        diction = {
            "name": self.name,
            "author": self.author
        }
        return diction
    
class Person:
    """Class handling the definition of who a person is
        to the web application"""
    
    __slots__ = ("username", "first_name", "last_name", "email", "address", "state", "is_admin", "is_staff")

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
    
class BorrowedBook:
    """Class to handle the borrowing of books
    to and from the web application"""

    __slots__ = ("email", "book_id", "return_date", "expected_return", "date_borrowed", "returned")

    def __init__(self, email: str, book_id: str,  return_date: datetime, expected_return: datetime, 
                 date_borrowed=datetime.now(), returned: bool=False) -> None:
        self.email = email
        self.book_id = book_id
        self.date_borrowed = date_borrowed
        self.expected_return = expected_return
        self.return_date = return_date
        self.returned = returned

    def to_dict(self):
        """ Converts the class's info into a dictionary
         for updating into MongoDB """
        diction = {
            "email": self.email,
            "book_id": self.book_id,
            "date_borrowed": self.date_borrowed,
            "expected_return": self.expected_return,
            "return_date": self.return_date,
            "returned": self.returned
        }
        return diction
    
class BorrowedBookInstance:
    """Class to handle the representation of 
    books in the web application."""

    __slots__ = ("name", "date_borrowed", "return_date", "expected_return", "returned", "slug")

    def __init__(self, name: str, date_borrowed: str, 
                 return_date: str, expected_return: str, returned: bool, slug: str) -> None:
        self.name = name
        self.date_borrowed = date_borrowed
        self.return_date = return_date
        self.expected_return = expected_return
        self.returned = returned
        self.slug = slug