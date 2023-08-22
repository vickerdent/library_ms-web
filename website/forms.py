from typing import Any, Dict, Mapping, Optional, Type, Union
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.utils import ErrorList

class SignUpForm(UserCreationForm):
    """Enables users to sign up to the web app."""
    email = forms.CharField(label="", widget=forms.EmailInput(
        attrs={"name": "email", "class": "form-control", "placeholder": "E-mail Address"}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={"name": "first_name", "class": "form-control", "placeholder": "First Name"}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={"name": "last_name", "class": "form-control", "placeholder": "Last Name"}))
    address = forms.CharField(label="", max_length=1000, widget=forms.TextInput(
        attrs={"name": "address", "class": "form-control", "placeholder": "Address"}))
    state = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={"name": "state", "class": "form-control", "placeholder": "State"}))
                             
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "address", "state", "password1", "password2")

    def __init__(self, *args: Any, **kwargs: Any):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>150 characters or fewer. Letters, digits and @, ., +, - or _ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<span class="form-text text-muted"><small>Enter a unique password made up of at least 8 characters: Letters, digits and special characters.</small></span>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	

class BookForm(forms.Form):
    """Create form using the Book class in model """

    YES_NO_CHOICES = [
        ("", "Select one"),
        (True, "True"),
        (False, "False"),
    ]

    name = forms.CharField(required=True, max_length=100, widget=forms.widgets.TextInput(
        attrs={"placeholder":"", "class":"form-control"}), label="Name")
    description = forms.CharField(required=True, widget=forms.widgets.Textarea(
        attrs={"placeholder":"", "class":"form-control"}), label="Description")
    isbn = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder":"", "class":"form-control"}), label="ISBN")
    page_count = forms.IntegerField(required=True, widget=forms.widgets.NumberInput(
        attrs={"placeholder":"", "class":"form-control"}), label="Page Count")
    issued_out = forms.ChoiceField(required=True, initial=False, choices=YES_NO_CHOICES, disabled=True,
                                   widget=forms.widgets.Select(
                                       attrs={"placeholder":"", "class":"form-select"}), label="Issued Out")
    author = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder":"", "class":"form-control"}), label="Author")
    year = forms.CharField(required=True, max_length=4, widget=forms.widgets.TextInput(
        attrs={"placeholder":"", "class":"form-control"}), label="Year Published")
    image = forms.ImageField(required=True, widget=forms.widgets.ClearableFileInput(
        attrs={"placeholder":"", "class":"form-control"}), label="Image")
    quantity = forms.IntegerField(required=True, widget=forms.widgets.NumberInput(
        attrs={"placeholder":"", "class":"form-control"}), label="Quantity")
    series = forms.ChoiceField(required=True, choices=YES_NO_CHOICES, widget=forms.widgets.Select(
        attrs={"placeholder":"", "class":"form-select", "id": "aseries"}), label="Part Of A Series")
    name_of_series = forms.CharField(required=False, widget=forms.widgets.TextInput(
        attrs={"placeholder":"", "class":"form-control", "id": "nameseries", "style": "display: none"}), label="Name Of Series")
    pos_in_series = forms.IntegerField(required=False, widget=forms.widgets.NumberInput(
        attrs={"placeholder":"", "class":"form-control", "id": "posseries", "style": "display: none"}), label="Position In Series")
    genre = forms.CharField(required=True, widget=forms.widgets.Textarea(
        attrs={"placeholder":"", "class":"form-control"}), label="Genre",
                            help_text='<span class="form-text text-muted"><small>Separate each genre \
                            value with commas. Each genre can have spaces in its name.</small></span>')

    def clean(self):
        cleaned_data = super().clean()
        series = cleaned_data.get("series")
        name_of_series = cleaned_data.get("name_of_series")
        pos_in_series = cleaned_data.get("pos_in_series")

        if series:
            if series == "True" and name_of_series == "":
                raise forms.ValidationError("Name of Series required!")
            elif series == "True" and pos_in_series == None:
                raise forms.ValidationError("Position in Series required!")
            elif series == "True" and pos_in_series < 1:
                raise forms.ValidationError("Position in Series must be greater than 0!")
            elif series == "False" and pos_in_series != None:
                raise forms.ValidationError("Book is not part of a series!")
            elif series == "False" and name_of_series:
                raise forms.ValidationError("Book is not part of a series!")
            
        return cleaned_data

    def clean_page_count(self):
        data = self.cleaned_data["page_count"]
        if data < 1:
            raise forms.ValidationError("Pages must be greater than 0!")
        return data
            
    def clean_quantity(self):
        data = self.cleaned_data["quantity"]
        if data < 0:
            raise forms.ValidationError("You can't have a negative number of books!")
        return data

# Create Edit Book Form
class EditBookForm(forms.Form):
    """Create form using the Book class in model """

    YES_NO_CHOICES = [
        ("", "Select one"),
        (True, "True"),
        (False, "False"),
    ]

    name = forms.CharField(required=True, max_length=100, widget=forms.widgets.TextInput(
        attrs={"placeholder":"", "class":"form-control"}), label="Name")
    description = forms.CharField(required=True, widget=forms.widgets.Textarea(
        attrs={"placeholder":"", "class":"form-control"}), label="Description")
    isbn = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder":"", "class":"form-control"}), label="ISBN")
    page_count = forms.IntegerField(required=True, widget=forms.widgets.NumberInput(
        attrs={"placeholder":"", "class":"form-control"}), label="Page Count")
    issued_out = forms.ChoiceField(required=True, choices=YES_NO_CHOICES, disabled=True,
                                   widget=forms.widgets.Select(
                                       attrs={"placeholder":"", "class":"form-select"}), label="Issued Out")
    author = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder":"", "class":"form-control"}), label="Author")
    year = forms.CharField(required=True, max_length=4, widget=forms.widgets.TextInput(
        attrs={"placeholder":"", "class":"form-control"}), label="Year Published")
    quantity = forms.IntegerField(required=True, widget=forms.widgets.NumberInput(
        attrs={"placeholder":"", "class":"form-control"}), label="Quantity")
    series = forms.ChoiceField(required=True, choices=YES_NO_CHOICES, widget=forms.widgets.Select(
        attrs={"placeholder":"", "class":"form-select", "id": "aseries"}), label="Part Of A Series")
    name_of_series = forms.CharField(required=False, widget=forms.widgets.TextInput(
        attrs={"placeholder":"", "class":"form-control", "id": "nameseries", "style": "display: none"}), label="Name Of Series")
    pos_in_series = forms.IntegerField(required=False, widget=forms.widgets.NumberInput(
        attrs={"placeholder":"", "class":"form-control", "id": "posseries", "style": "display: none"}), label="Position In Series")
    genre = forms.CharField(required=True, widget=forms.widgets.Textarea(
        attrs={"placeholder":"", "class":"form-control"}), label="Genre",
                            help_text='<span class="form-text text-muted"><small>Separate each genre \
                            value with commas. Each genre can have spaces in its name.</small></span>')

    def clean(self):
        cleaned_data = super().clean()
        series = cleaned_data.get("series")
        name_of_series = cleaned_data.get("name_of_series")
        pos_in_series = cleaned_data.get("pos_in_series")

        if series:
            if series == "True" and name_of_series == "":
                raise forms.ValidationError("Name of Series required!")
            elif series == "True" and pos_in_series == None:
                raise forms.ValidationError("Position in Series required!")
            elif series == "True" and pos_in_series < 1:
                raise forms.ValidationError("Position in Series must be greater than 0!")
            elif series == "False" and pos_in_series != None:
                raise forms.ValidationError("Book is not part of a series!")
            elif series == "False" and name_of_series:
                raise forms.ValidationError("Book is not part of a series!")
            
        return cleaned_data

    def clean_page_count(self):
        data = self.cleaned_data["page_count"]
        if data < 1:
            raise forms.ValidationError("Pages must be greater than 0!")
        return data
            
    def clean_quantity(self):
        data = self.cleaned_data["quantity"]
        if data < 0:
            raise forms.ValidationError("You can't have a negative number of books!")
        return data

# create form for editing images

class EditImageForm(forms.Form):
    """Form to edit images for books """
    image = forms.ImageField(required=True, widget=forms.widgets.ClearableFileInput(
        attrs={"placeholder":"", "class":"form-control"}), label="Image")
    
class ConfirmCodeForm(forms.Form):
    """Form to confirm code sent to new users """
    code = forms.CharField(required=True, max_length=12, widget=forms.widgets.TextInput(
        attrs={"placeholder":"", "class":"form-control"}), label="Enter Confirmation Code")

class BorrowBookForm(forms.Form):
    """Create form for borrowing books """
    DURATION_CHOICES = [
        ("", "Select one"),
        ("1 Day", "1 Day"),
        ("3 Days", "3 Days"),
        ("1 Week", "1 Week"),
        ("3 Weeks", "3 Weeks"),
    ]

    duration = forms.ChoiceField(required=True, choices=DURATION_CHOICES, widget=forms.widgets.Select(
        attrs={"placeholder":"", "class":"form-select"}), label="Length Of Time")
    

class RequestABookForm(forms.Form):
    """Create form using the Request A Book class in model """

    name = forms.CharField(required=True, max_length=150, widget=forms.widgets.TextInput(
        attrs={"placeholder":"", "class":"form-control"}), label="Name of Book")
    author = forms.CharField(required=True, max_length=150, widget=forms.widgets.TextInput(
        attrs={"placeholder":"", "class":"form-control"}), label="Author of Book")