from datetime import datetime, timedelta
import random

def code_generator():
    """Generate random code to send via email to new user"""
    alpha_num_list = (
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M'
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W' 'X', 'Y', 'Z'
        )
    first_elem = random.choice(alpha_num_list)
    second_elem = random.randint(1, 9)
    third_elem = random.randint(1, 9)
    fourth_elem = random.randint(1, 9)
    fifth_elem = random.randint(1, 9)
    sixth_elem = random.randint(1, 9)

    char_list = str(first_elem) + str(second_elem) + str(third_elem) + \
    str(fourth_elem) + str(fifth_elem) + str(sixth_elem)

    return char_list

def calculate_return(duration):
    """Calculate return date
    for borrowed book for a user"""
    today = datetime.now()
    return_date = today
    if duration == "1 Day":
        return_date = today + timedelta(days=1)
    elif duration == "3 Days":
        return_date = today + timedelta(days=3)
    elif duration == "1 Week":
        return_date = today + timedelta(weeks=1)
    elif duration == "3 Weeks":
        return_date = today + timedelta(weeks=3)
    return return_date

def correct_id(name) -> str:
    """ Used to introduce correct
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

def change_image_name(image, book_id):
    image_dot = str(image.name).rfind(".")
    
    # Include the dot, and give the whole extension
    image_ext = image.name[image_dot:]
    return str(book_id) + str(image_ext)
