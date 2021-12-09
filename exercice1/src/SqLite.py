import os
import sqlite3
from Spell import *

db_name = 'spell.db'

create_query = '''CREATE TABLE spell (
                            name TEXT PRIMARY KEY,
                            level INTEGER,
                            components TEXT,
                            spell_resistance  INTEGER,
                            class_linked TEXT);'''

insert_query = ''' INSERT OR REPLACE INTO spell(name,level,components,spell_resistance,class_linked)
             VALUES(?,?,?,?,?) '''

drop_table_query = '''DROP TABLE IF EXISTS spell'''

select_spell_query='''
select * from spell 
WHERE 
components = 'V'
AND (
class_linked LIKE '%wizard 4%' 
OR class_linked LIKE '%wizard 3%'
OR class_linked LIKE '%wizard 2%' 
OR class_linked LIKE '%wizard 1%'
OR class_linked LIKE '%wizard 0%'
 )
'''


class SqLite():
    def __init__(self, db_name):

        try:
            self.sqliteConnection = sqlite3.connect(db_name)
            self.create_base()

        except sqlite3.Error as error:
            print("can't open dataBase", error)
            self.sqliteConnection.close()

    def create_base(self):

        try:

            cursor = self.sqliteConnection.cursor()
            #cursor.execute(drop_table_query)
            cursor.execute(create_query)
            self.sqliteConnection.commit()
            cursor.close()
            print("table creation done")
        except sqlite3.Error as error:
            print("can't create SqliteTable", error)
            self.sqliteConnection.close()

    def put_spell(self,spell_class):

        try:
            self.sqliteConnection = sqlite3.connect(db_name)
            cursor = self.sqliteConnection.cursor()
            cursor.execute(insert_query,(spell_class.name,spell_class.level,':'.join(spell_class.components),spell_class.resistance,spell_class.classLinked,))
            self.sqliteConnection.commit()
            cursor.close()
            print("Data put in sqlLite")
        except sqlite3.Error as error:
            print("can't put data", error)


    def select_spell(self):
        self.sqliteConnection = sqlite3.connect(db_name)
        cursor = self.sqliteConnection.cursor()
        cursor.execute(select_spell_query)
        result = cursor.fetchall()
        cursor.close()

        for r in result:
            print(r)

    def drop_table(self):
        try:
            self.sqliteConnection = sqlite3.connect(db_name)
            cursor = self.sqliteConnection.cursor()
            cursor.execute(drop_table_query)
            self.sqliteConnection.commit()
            cursor.close()
            print("table drop done")
            self.create_base()

        except sqlite3.Error as error:
            print("can't drop table", error)
