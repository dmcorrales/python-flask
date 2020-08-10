from peewee import *
import datetime
from collections import OrderedDict 

db = SqliteDatabase('blog.sql')

class Entry(Model):
    #Contenido
    content = TextField()
    #Fecha - timestamp
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

def add_entry():
    """"""
    
def view_entries():
    """"""  
def delete_entry():
    """"""

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries)
])

def menu_loop():
    choice = None

    while choice != 'q':
        print("Presione 'q' para salir ")
        for key,value in menu.items():
            print('{}| {}'.format(key,value.__doc__))
        choice = input('Eleccion: ').lower().strip()

        if choice in menu:
            menu[choice]()


def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)

if __name__ == "__main__":
    initialize()
    menu_loop()