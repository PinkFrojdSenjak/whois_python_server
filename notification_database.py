import sqlite3
import string
import random
def id_generator(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

con = sqlite3.connect('notifications.db', check_same_thread=False)

curr = con.cursor()

class Notifications:
    
    def _insert_token(self, url, token):
        curr.execute(
            '''SELECT 
                * FROM Subscriptions
                WHERE url = ?
                AND token = ?
            ''', (url, token)
        )
        rows = curr.fetchall()
        if rows:
            return False
        random_string = id_generator()

        curr.execute(
        """
            INSERT INTO Subscriptions(id,url,token)
            VALUES (?,?,?)
        """, (random_string, url, token))
        con.commit()
        return True

    def _insert_email(self, url, email):
        curr.execute(
            '''SELECT 
                * FROM Subscriptions
                WHERE url = ?
                AND email = ?
            ''', (url, email)
        )
        rows = curr.fetchall()
        if rows:
            return False
        random_string = id_generator()

        curr.execute(
        """
            INSERT INTO Subscriptions(id,url,email)
            VALUES (?,?,?)
        """, (random_string, url, email))
        con.commit()
        return True

    def subscribe(self, url, email, token):
        if email is None:
            return self._insert_token(url, token)
        else:
            return self._insert_email(url, email)

    def unsubscribe_push(self, token):
        curr.execute("DELETE FROM Subscriptions WHERE token = ? ", (token,))
        con.commit()

    def unsubscribe_email(self, id):
        curr.execute("DELETE FROM Subscriptions WHERE id = ? ", (id,))
        con.commit()

    def change_token(self, old, new):
        curr.execute('UPDATE Subscriptions SET token = ? WHERE token = ?', (new, old))
        con.commit()

if __name__ == "__main__":
    temo_con = sqlite3.connect('temp.db')
    temp_curr = temo_con.cursor()
    temp_curr.execute('SELECT COUNT( *) FROM Notifications')
    print(temp_curr.fetchall())