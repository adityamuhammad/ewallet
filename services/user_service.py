from sqlalchemy import text

class UserService:
    def __init__(self, engine):
        self.engine = engine
    
    def get_user_by_email(self, email):
        conn = self.engine.connect()
        select_user = text("""
            select id, password from user where email = :email limit 1
        """)
        user = conn.execute(select_user, email=email).fetchone()
        conn.close()
        if user is not None:
            return {
                'id': user[0],
                'password': user[1]
            }
        else:
            return None

    def get_user_by_id(self, id):
        conn = self.engine.connect()
        select_user = text("""
            select username from user where id = :id limit 1
        """)
        user = conn.execute(select_user, id=id).fetchone()
        conn.close()
        if user is not None:
            return {
                'username': user[0],
            }
        else:
            return None
