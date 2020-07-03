import sqlite3
import json

connect = sqlite3.connect('members.db')
cursor = connect.cursor()

class MemberInfo:
    def __init__(self, id, first_name=None, username=None, lang=None, uzcard=None, qiwi=None):
        self.id = id
        self.first_name = first_name
        self.username = username
        self.lang = lang
        self.uzcard =uzcard
        self.qiwi = qiwi

#Methods for add data
    def add_id(self):
        cursor.execute("INSERT INTO members_info (id) VALUES(?);", (self.id,))
        connect.commit()

    def add_first_name(self):
        cursor.execute("INSERT INTO members_info (first_name) VALUES(?);", (self.first_name,))
        connect.commit()

    def add_language(self):
        cursor.execute("INSERT INTO members_info (lang) VALUES(?);", (self.lang,))
        connect.commit()

    def add_uzcard(self):
        cursor.execute("INSERT INTO members_info (uzcard) VALUES(?);", (self.uzcard,))
        connect.commit()

    def add_qiwi(self):
        cursor.execute("INSERT INTO members_info (qiwi) VALUES(?);", (self.qiwi,))
        connect.commit()

#Methods for get data
    def get_first_name(self):
        cursor.execute("SELECT first_name FROM members_info WHERE id = (?);", (self.id,))
        connect.commit()

    def get_language(self):
        cursor.execute("SELECT lang FROM members_info WHERE id = (?);", (self.id,))
        connect.commit()

    def get_uzcard(self):
        cursor.execute("SELECT uzcard FROM members_info WHERE id = (?)", (self.id,))
        connect.commit()

    def get_qiwi(self):
        cursor.execute("SELECT qiwi FROM members_info WHERE id = (?)", (self.id,))
        connect.commit()


connect.close()