from sqlalchemy import text
class WalletService:
    def __init__(self, engine, data):
        self.engine = engine
        self.data = data
    
    def topup(self):
        conn = self.engine.connect()
        data = self.data
        trans = conn.begin()
        try:
            q_user_balance = text(
                """
                    select id, balance from user_balance where user_id = :user_id limit 1
                """
            )
            user_balance = conn.execute(q_user_balance, user_id=data['user_id']).fetchone()
            user_balance_id, balance_before = 0, 0
            if user_balance:
                user_balance_id, balance_before = user_balance

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
            else:
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
                balance_before=balance_before,
                balance_after=balance_before + data['amount'],
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
    
    def check_balance(self):
        amount = self.data['amount']
        user_id = self.data['user_id']
        conn = self.engine.connect()
        q_user_balance = text(
            """
                select balance from user_balance where user_id = :user_id limit 1
            """
        )
        user_balance = conn.execute(q_user_balance, user_id=user_id).fetchone()
        conn.close()
        if user_balance:
            balance = user_balance[0]
            if amount > 0 and balance >= amount:
                return True

        return False

    def transfer(self):
        conn = self.engine.connect()
        data = self.data
        trans = conn.begin()
        try:
            q_bank_balance = text(
                """
                    select id, balance from bank_balance where code = :code limit 1
                """
            )
            bank_balance = conn.execute(q_bank_balance, code=data['code']).fetchone()
            bank_balance_id, bank_balance_before = 0, 0
            if bank_balance:
                bank_balance_id, bank_balance_before = bank_balance
                update_bank_balance = text(
                    """
                        update bank_balance 
                            set balance = balance + :amount, 
                                balance_achieve = balance_achieve + :amount 
                            where id = :bank_balance_id
                    """
                )
                conn.execute(update_bank_balance, 
                    amount=data['amount'],
                    bank_balance_id=bank_balance_id
                )
            else:
                insert_bank_balance = text(
                    """
                        insert into bank_balance 
                            (balance, balance_achieve, code, enable)
                        values
                            (:balance, :balance_achieve, :code, :enable)
                    """
                )
                conn.execute(insert_bank_balance, 
                    balance=data['amount'],
                    balance_achieve=data['amount'],
                    code=data['code'],
                    enable=True
                )
                bank_balance_id = conn.execute("select last_insert_id()").fetchone()[0]

            insert_bank_balance_history = text(
                """
                    insert into bank_balance_history
                        (
                            bank_balance_id, balance_before, balance_after,
                            activity, type, ip, location, user_agent, author
                        )
                    values
                        (
                            :bank_balance_id, :balance_before, :balance_after,
                            :activity, :type, :ip, :location, :user_agent, :author
                        )
                """
            )
            conn.execute(insert_bank_balance_history, 
                bank_balance_id=bank_balance_id,
                balance_before=bank_balance_before,
                balance_after=bank_balance_before + data['amount'],
                activity='transfer from user balance to bank ' + data['code'],
                type='debit',
                ip=data['ip'],
                location=data['location'],
                user_agent=data['user_agent'],
                author=data['author']
            )

            q_user_balance = text(
                """
                    select id, balance from user_balance where user_id = :user_id limit 1
                """
            )
            user_balance = conn.execute(q_user_balance, user_id=data['user_id']).fetchone()
            user_balance_id,user_balance_before = user_balance
            update_user_balance = text(
                """
                    update user_balance set balance = balance - :amount where user_id = :user_id
                """
            )
            conn.execute(update_user_balance, 
                amount=data['amount'],
                user_id=data['user_id']
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
                balance_before=user_balance_before,
                balance_after=user_balance_before - data['amount'],
                activity='transfer to bank ' +  data['code'],
                type='credit',
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


