from sqlalchemy import text

class UserService:
    def __init__(self, engine):
        self.engine = engine
    
    def get_user(self, email):
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
