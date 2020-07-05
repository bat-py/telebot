import sqlite3
import json



class MemberInfo:
    def __init__(self, id, first_name=None, username=None, lang=None, uzcard=None, qiwi=None):
        self.id = str(id)
        self.first_name = str(first_name)
        self.username = username
        self.lang = str(lang)
        self.uzcard = str(uzcard)
        self.qiwi = str(qiwi)
        self.connect = sqlite3.connect('members.db')
        self.cursor = self.connect.cursor()
        self.non = None
#Methods for add data
    def add_id(self):
        self.cursor.execute(f"INSERT INTO members_info(id) VALUES({self.id});")
        self.connect.commit()

    def add_first_name(self):
        self.cursor.execute('''
                            UPDATE members_info
                            SET first_name=(?)
                            WHERE id=(?)
                            ''', (self.first_name, self.id))
        self.connect.commit()

    def add_username(self):
        self.cursor.execute("UPDATE members_info SET username = (?) WHERE id = (?);", (self.username, self.id))
        self.connect.commit()

    def add_language(self):
        self.cursor.execute(f"UPDATE members_info SET lang = (?) WHERE id = (?);", (self.lang, self.id))
        self.connect.commit()

    def add_uzcard(self):
        self.cursor.execute("UPDATE members_info SET uzcard = (?) WHERE id = (?);", (self.uzcard, self.id))
        self.connect.commit()

    def add_qiwi(self):
        self.cursor.execute("UPDATE members_info SET qiwi = (?) WHERE id = (?);", (self.qiwi, self.id))
        self.connect.commit()

#Methods for get data
    def get_lang(self):
        self.cursor.execute("SELECT lang FROM members_info WHERE id = (?);", (self.id,))
        return self.cursor.fetchone()[0]


    def get_first_name(self):
        self.cursor.execute("SELECT first_name FROM members_info WHERE id = (?);", (self.id,))
        return self.cursor.fetchone()

    def get_language(self):
        self.cursor.execute("SELECT lang FROM members_info WHERE id = (?);", (self.id,))
        return self.cursor.fetchone()

    def get_uzcard(self):
        self.cursor.execute("SELECT uzcard FROM members_info WHERE id = (?);", (self.id,))
        return self.cursor.fetchone()[0]

    def get_qiwi(self):
        self.cursor.execute("SELECT qiwi FROM members_info WHERE id = (?);", (self.id,))
        return self.cursor.fetchone()[0]

#delete members
    def del_mem(self):
        self.cursor.execute("DELETE FROM members_info WHERE id = (?);", (self.id,))
        self.connect.commit()


    def del_uzcard_qiwi(self):
        self.cursor.execute("UPDATE members_info SET uzcard = (?), qiwi = (?) WHERE id = (?)", (None, None, self.id))
        self.connect.commit()
