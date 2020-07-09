# -*- coding: utf-8 -*-
import sqlite3
import random

class MemberInfo:
    def __init__(self, id, first_name=None, username=None, lang=None, uzcard=None, qiwi=None, id_application=None, type=None, rubl=None, sum=None):
        self.id = str(id)
        self.first_name = str(first_name)
        self.username = username
        self.lang = str(lang)
        self.uzcard = str(uzcard)
        self.qiwi = str(qiwi)
        self.connect = sqlite3.connect('/home/crow/PycharmProjects/telebot/members.db')
        self.cursor = self.connect.cursor()
        self.non = None
        self.type = type
        self.id_application = id_application
        self.rubl = rubl
        self.sum = sum
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
        self.cursor.execute("UPDATE members_info SET lang = (?) WHERE id = (?);", (self.lang, self.id))
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

    def get_nice_uzcard(self):
        self.cursor.execute("SELECT uzcard FROM members_info WHERE id = (?);", (self.id,))
        uzcard = str(self.cursor.fetchone()[0])
        nice_uzcard = ' '.join([f"{uzcard[i:i + 4]}" for i in range(0, 16, 4)]).strip()
        return nice_uzcard

    def get_nice_qiwi(self):
        self.cursor.execute("SELECT qiwi FROM members_info WHERE id = (?);", (self.id,))
        qiwi = str(self.cursor.fetchone()[0])
        nice_qiwi = '-'.join([qiwi[0:3], qiwi[3:5], qiwi[5:8], qiwi[8:10], qiwi[10:12]])
        return nice_qiwi


#delete members
    def del_mem(self):
        self.cursor.execute("DELETE FROM members_info WHERE id = (?);", (self.id,))
        self.connect.commit()


    def del_uzcard_qiwi(self):
        self.cursor.execute("UPDATE members_info SET uzcard = (?), qiwi = (?) WHERE id = (?)", (None, None, self.id))
        self.connect.commit()






#Applications:
    def get_id_application(self):
        self.cursor.execute("SELECT id_application FROM applications WHERE id_application = (?)", (self.id_application,))
        return self.cursor.fetchone()


    def add_application(self):
        self.cursor.execute("INSERT INTO applications (id, id_applicaion) VALUES (?, ?);", (self.id, self.id_application))
        self.connect.commit()




#Working applications
    def get_id_working_application(self):
        self.cursor.execute("SELECT id_application FROM working_applications WHERE id = (?)", (self.id,))
        return self.cursor.fetchone()

    def add_working_application(self):
        self.cursor.execute("INSERT INTO working_applications (id, id_application) VALUES(?, ?);", (self.id, self.id_application))
        self.connect.commit()

    def add_summa_rubl_uzs(self):
        self.cursor.execute("UPDATE working_applications SET rubl = (?), sum = (?) WHERE id = (?)", (self.rubl, self.sum, self.id ))
        self.connect.commit()

    def add_type_change(self):
        self.cursor.execute("UPDATE working_applications SET type_change = (?) WHERE id = (?)", (self.type ,self.id))
        self.connect.commit()

    def get_summa_uzs_rubl(self):
        self.cursor.execute("SELECT sum, rubl FROM working_applications WHERE id = (?)", (self.id,))
        return self.cursor.fetchone()