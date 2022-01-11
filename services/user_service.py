from sqlalchemy import text
from database.database_factory import DatabaseFactory

class UserService:
    def __init__(self):
        self.engine = DatabaseFactory.get()
    
    def get_user_by_email(self, email):
        conn = self.engine.connect()
        select_user = text("""
            select id, password from user where email = :email limit 1
        """)
        user = conn.execute(select_user, email=email).fetchone()
        conn.close()
        if user is not None:
            return { 'id': user[0], 'password': user[1] }
        return None

    def get_user_by_id(self, id):
        conn = self.engine.connect()
        select_user = text("""
            select username from user where id = :id limit 1
        """)
        user = conn.execute(select_user, id=id).fetchone()
        conn.close()
        if user is not None:
            return { 'username': user[0], }
        return None
