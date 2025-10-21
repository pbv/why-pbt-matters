# -------------------------------------------------------
# A SQLite database for users and emails
#
# Pedro Vasconcelos, 2025
# -------------------------------------------------------
import sqlite3

class UserDB:
    def __init__(self):
        self.con = sqlite3.connect(":memory:")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE users("
                         "         id INTEGER PRIMARY KEY,"
                         "         user INTEGER, email TEXT,"
                         "         UNIQUE (user,email))")

    def close(self):
        "Close the DB connection."
        self.con.close()
        
    def add(self, user, email):
        "Add another email for a user."
        self.cur.execute("INSERT OR IGNORE "
                         "INTO users(user,email) VALUES (?,?)",
                         (user,email))
        self.con.commit()
        
    def get(self, user):
        "Get all emails for a user."
        res = self.cur.execute("SELECT email FROM users "
                               "WHERE user=?", (user,))
        answer = [ row[0] for row in res.fetchall() ]
        return answer

    def remove(self, user, email):
        "Remove an email from a user."
        self.cur.execute("DELETE FROM users "
                         "WHERE user=? AND email=?",
                         (user,email))
    
    def delete(self, user):
        "Remove all emails from a user."
        self.cur.execute("DELETE FROM users "
                         "WHERE user=?", (user,))
