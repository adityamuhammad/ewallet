from sqlalchemy import text
class WalletService:
    def __init__(self, engine):
        self.engine = engine
    
    def topup(self,data):
        conn = self.engine.connect()
        trans = conn.begin()
        try:
            q_user_balance = text(
                """
                    select id, balance from user_balance where user_id = :user_id limit 1
                """
            )
            user_balance = conn.execute(q_user_balance, user_id=data.get('user_id')).fetchone()
            if user_balance:
                user_balance_id = user_balance[0]
                balance_before = user_balance[1]

                update_user_balance = text(
                    """
                        update user_balance 
                            set balance = balance + :amount, 
                                balance_achieve = balance_achieve + :amount 
                            where id = :user_balance_id
                    """
                )
                conn.execute(update_user_balance, 
                    amount=data['amount'],
                    user_balance_id=user_balance_id
                )
                insert_user_balance_history = text(
                    """
                        insert into user_balance_history
                            (
                                user_balance_id, balance_before, balance_after,
                                activity, type, ip, location, user_agent, author
                            )
                        values
                            (
                                :user_balance_id, :balance_before, :balance_after,
                                :activity, :type, :ip, :location, :user_agent, :author
                            )
                    """
                )
                conn.execute(insert_user_balance_history, 
                    user_balance_id=user_balance_id,
                    balance_before=balance_before,
                    balance_after=balance_before + data['amount'],
                    activity='topup',
                    type=data['type'],
                    ip=data['ip'],
                    location=data['location'],
                    user_agent=data['user_agent'],
                    author=data['author']
                )
            else:
                balance_before = 0
                user_balance_id = 0
                insert_user_balance = text(
                    """
                        insert into user_balance
                            (user_id, balance, balance_achieve)
                        values (:user_id, :balance, :balance_achieve)
                    """
                )
                conn.execute(insert_user_balance, 
                    user_id=data['user_id'],
                    balance=data['amount'],
                    balance_achieve=data['amount'],
                    user_balance_id=user_balance_id
                )
                user_balance_id = conn.execute("select last_insert_id()").fetchone()[0]
                insert_user_balance_history = text(
                    """
                        insert into user_balance_history
                            (
                                user_balance_id, balance_before, balance_after,
                                activity, type, ip, location, user_agent, author
                            )
                        values
                            (
                                :user_balance_id, :balance_before, :balance_after,
                                :activity, :type, :ip, :location, :user_agent, :author
                            )
                    """
                )
                conn.execute(insert_user_balance_history, 
                    user_balance_id=user_balance_id,
                    balance_before=0,
                    balance_after=0 + data['amount'],
                    activity='topup',
                    type=data['type'],
                    ip=data['ip'],
                    location=data['location'],
                    user_agent=data['user_agent'],
                    author=data['author']
                )

            trans.commit()
        except:
            trans.rollback()
            raise
        finally:
            conn.close()

