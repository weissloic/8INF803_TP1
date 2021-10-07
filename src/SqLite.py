import os
import sqlite3
from Spell import *

db_name = 'SQLite.db'

create_query = '''CREATE TABLE spell (
                            name TEXT ,
                            components TEXT,
                            spell_resistance  INTEGER );'''

drop_table_query = '''DROP TABLE IF EXISTS spell'''


class SqLite():
    def __init__(self):

        try:
            self.sqliteConnection = sqlite3.connect(db_name)
            print("SQLite up")
            self.create_base()
        except sqlite3.Error as error:
            print("can't open dataBase", error)
            self.sqliteConnection.close()

    def create_base(self):

        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute(drop_table_query)
            cursor.execute(create_query)
            self.sqliteConnection.commit()
            cursor.close()
            print("table creation done")
        except sqlite3.Error as error:
            print("can't create SqliteTable", error)
            self.sqliteConnection.close()

    def put_spell(self,spell_class):
        query = ''' INSERT INTO spell(name,components,spell_resistance)
             VALUES(?,?,?) '''
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute(query,(spell_class.name,spell_class.components,spell_class.resistance,))
            self.sqliteConnection.commit()
            cursor.close()
            print("Data put done")
        except sqlite3.Error as error:
            print("can't put data", error)


    def close_sql(self):
        self.sqliteConnection.close()
