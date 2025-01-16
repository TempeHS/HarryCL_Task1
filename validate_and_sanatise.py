from flask import current_app as app
import re
import bcrypt
import html
import database_manager as dbHandler


def hash(password: str) -> str:
    salt = bcrypt.gensalt()
    encoded_password = password.encode()
    hashed_password = bcrypt.hashpw(password=encoded_password, salt=salt)
    return hashed_password.decode()

def verify_password(stored_password: str, provided_password: str) -> bool:
    return bcrypt.checkpw(provided_password.encode(), stored_password.encode())

def sanitize_input(user_input: str) -> str:
    sanitized_input = html.escape(user_input)
    sanitized_input = re.sub(r"[\'\";]", "", sanitized_input)
    sanitized_input = re.sub(r"[^a-zA-Z0-9\s]", "", sanitized_input)
    return sanitized_input

def validate_password(devtag: str, password: str) -> dict:
    errors = {
        'length': False,
        'upper': False,
        'lower': False,
        'number': False,
        'special': False,
        'duplicate': False
    }
    if dbHandler.userExists(devtag):
        errors['duplicate'] = True
    if len(password) < 8:
        errors['length'] = True
    if not any(char.isupper() for char in password):
        errors['upper'] = True
    if not any(char.islower() for char in password):
        errors['lower'] = True
    if not any(char.isdigit() for char in password):
        errors['number'] = True
    if not any(char in '!@#$%^&*' for char in password):
        errors['special'] = True
    return errors