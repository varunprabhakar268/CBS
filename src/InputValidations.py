from datetime import datetime
import re


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
