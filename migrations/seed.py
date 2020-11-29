from flask_bcrypt import generate_password_hash
from sqlalchemy import create_engine, text
from os import environ

engine = create_engine(environ.get('DATABASE_URI_DEV'))

with engine.connect() as conn:
    conn.execute(text(
        """
        INSERT INTO user
            (username, email, password)
        VALUES (:username, :email, :password)
        """
    ), username='aditya', email='aditya@ewallet.com', password=generate_password_hash('password').decode('utf-8'))
    print("success..")
