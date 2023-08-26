# Library Management System

This project is a product of Python + Django, spiced with Bootstrap and backed by MongoDB and PostgreSQL.

## NOTES

* I tried to make it approach a semi-production environment, hence PostgreSQL database is provided by ElephantSQL, MongoDB by MongoDB Atlas, storage by BackBlaze Cloud Storage and email service by Google.
* Note that the models in this project are not typical models, since I used MongoDB as my main database, and MongoDB doesn't play well with Django, at least not yet.
* To make this work, you need to create accounts (they're free to do) with the aforementioned third parties: MongoDB Atlas, ElephantSQL and BackBlaze Clound Storage, if you don't have them.

## Quick Start
To get this project up and running locally on your computer, after downloading:
1. Set up and activate a python environment. If you're within Visual Studio Code, you can do everything within the terminal:
    ```
    cd ..
    python3 -m venv venv
    venv\Script\activate
    cd library_ms_web (the name of your folder) 
    ```
1. Create accounts with aforementioned provides: MongoDB Atlas, ElephantSQL, Backblaze Cloud Storage. You can move to a higher tier, if you have the chop.
1. Create a .env file with the following keys and values for your accounts:
    ```
    MONGODB_URI=MongoDB Atlas URI to connect a database

    EMAIL_SENDER=Email address you want to send emails from
    EMAIL_PASSWORD=key provided by Google from app keys. Ensure 2-Factor authentication is set.

    BACKBLAZE_APPLICATION_KEY_ID=This is obtained when creating a bucket in BackBlaze
    BACKBLAZE_APPLICATION_KEY=You get this as well
    BACKBLAZE_BUCKET=The name of the created bucket

    PG_USER=This is both the name of the user and the name of the database on ElephantSQL
    PG_PASSWORD=Given at Elephant SQL
    PG_HOST=Referred to as 'Server' on Elephant SQL
    ```
1. Assuming you have Python setup, run the following commands (if you're on Windows you may use `py` or `py -3` instead of `python` to start Python):
    ```
    pip3 install -r requirements.txt
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py collectstatic
    python3 manage.py createsuperuser # Create a superuser, take note of the email address and username
    python3 manage.py runserver
    ```
1. Open a browser to `http://127.0.0.1:8000` to see the site.
1. Sign up an account on the site
1. In MongoDB Atlas, the `Users` collection, add the superuser's record, and set every boolean to `True`
1. Add books using the `sample_data`
