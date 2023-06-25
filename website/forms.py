from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.CharField(label="", 
                             widget=forms.EmailInput(attrs={"name": "email", "class": "form-control", "placeholder": "E-mail Address"}))
    first_name = forms.CharField(label="", max_length=100, 
                             widget=forms.TextInput(attrs={"name": "first_name", "class": "form-control", "placeholder": "First Name"}))
    last_name = forms.CharField(label="", max_length=100, 
                             widget=forms.TextInput(attrs={"name": "last_name", "class": "form-control", "placeholder": "Last Name"}))
    address = forms.CharField(label="", max_length=1000, 
                             widget=forms.TextInput(attrs={"name": "address", "class": "form-control", "placeholder": "Address"}))
    state = forms.CharField(label="", max_length=100, 
                             widget=forms.TextInput(attrs={"name": "state", "class": "form-control", "placeholder": "State"}))
                             
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


# Create Add User Form
# class EditUserForm(forms.Form):
#     first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"First Name", "class":"form-control"}), label="")
#     last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Last Name", "class":"form-control"}), label="")
#     email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Email", "class":"form-control", "readonly": "True"}), label="")
#     phone = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Phone", "class":"form-control"}), label="")
#     address = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Address", "class":"form-control"}), label="")
#     city = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"City", "class":"form-control"}), label="")
#     state = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"State", "class":"form-control"}), label="")
#     zipcode = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Zipcode", "class":"form-control"}), label="")
