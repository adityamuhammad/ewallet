from flask_bcrypt import generate_password_hash, check_password_hash
import re
import uuid

def generate_username(firstname, lastname):
    return firstname[0].lower() + re.compile('[^a-zA-Z]').sub('', lastname).lower()  + '-' + uuid.uuid4().hex

def generate_password(password):
    return generate_password_hash(password).decode('utf-8')

def check_password(password_db, password):
    return check_password_hash(password_db, password)