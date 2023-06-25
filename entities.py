from datetime import datetime

class Book:
    def __init__(self, id: str, name: str, description: str, isbn: str, page_count: int, 
                 issued_out: bool, author: str, year: int, issuee: list=None, image=None, date_issued=None):
        self.id = id
        self.name = name
        self.description = description
        self.isbn = isbn
        self.page_count = page_count
        self.issued_out = issued_out
        self.author = author
        self.year = year
        self.issuee = issuee
        self.image = image
        self.date_issued = date_issued

    def to_dict(self):
        diction = {
            "ID": self.id, 
            "Name": self.name,
            "Description": self.description,
            "ISBN": self.isbn, 
            "Page Count": self.page_count,
            "Issued Out": self.issued_out,
            "Author": self.author,
            "Year Published": self.year,
            "Book Image": self.image,
            "Date Issued": self.date_issued}
        return diction
    
    def hide_id(self):
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
    
class Person:
    def __init__(self, username: str, first_name: str, last_name: str, email: str, address: str, state: str, is_admin=False, is_staff=False):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.state = state
        self.is_admin = is_admin
        self.is_staff = is_staff

    def to_dict(self):
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