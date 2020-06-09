from datetime import datetime
import re


def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        print("\tInvalid date. Please try again. ")
        return False


def validate_email(email):
    """
    check if the entered email is valid or not.
    :param email:
    :return:
    """
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):
        return True
    else:
        print("Invalid Email")
        return False
