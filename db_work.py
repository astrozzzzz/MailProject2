import sqlite3
import time

DB_NAME = 'server_db.sqlite'


class DBHandler:
    def __init__(self):
        self.db = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.cur = self.db.cursor()

    def insert_user(self, username):
        if self.cur.execute(f"SELECT name FROM users WHERE name = '{username}'").fetchone() is None:
            all_users = [i for i in self.cur.execute(f"SELECT * FROM users")]
            if len(all_users) == 0:
                self.cur.execute(f"INSERT INTO users VALUES (1, '{username}')")
            else:
                self.cur.execute(f"INSERT INTO users VALUES ({all_users[-1][0] + 1}, '{username}')")
            self.db.commit()
            return True
        else:
            return False

    def check_user(self, username):
        if self.cur.execute(f"SELECT name FROM users WHERE name = '{username}'").fetchone() is None:
            return False
        else:
            return True

    def insert_mail(self, sender, addressee, title, main_text):
        date = str(time.strftime('%H:%M %x'))
        self.cur.execute(f"INSERT INTO mails VALUES ('{sender}', '{addressee}', '{date}', '{title}', '{main_text}')")
        self.db.commit()

    def mails_to_user(self, addressee):
        mails = self.cur.execute(f"""SELECT sender, addressee, date, title, main_text FROM mails 
        WHERE addressee = '{addressee}'""")
        return mails

    def mails_from_user(self, user):
        mails = self.cur.execute(f"""SELECT sender, addressee, date, title, main_text FROM mails 
        WHERE sender = '{user}'""")
        return mails

    def delete_mail(self, sender, addressee, date, title, main_text):
        self.cur.execute(f"""DELETE FROM mails WHERE sender = '{sender}' AND addressee = '{addressee}' AND date = '{date}' AND title = '{title}' AND main_text = '{main_text}'""")
        self.db.commit()

    def buff(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS mail (
            id INT,
            sender TEXT,
            addressee TEXT,
            date TEXT,
            title TEXT,
            main_text TEXT
        )""")
        self.db.commit()

# a = DBHandler()
# for i in a.mails_from_user('Ura'):
#     print(i)
# a.delete_mail(*['Ura', 'a', '00:17 11/15/21', 'Првет, это Юра', 'фвфвфвфвфыв'])



