from peewee import *
import datetime
import sys
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
    print("Introduce tu registro. Presiona CTRL + D cuando termines")

    data = sys.stdin.read().strip()

    if data:
        if input('Guardar entrada? [Yn]').lower() != 'n':
            Entry.create(content=data)
            print('Guardado exitosamente')
    
def view_entries(filter_entry=None):
    entries = None
    if(filter_entry!=None):
        entries = Entry.select().where(Entry.content.contains(filter_entry))
    else:    
        entries = Entry.select().order_by(Entry.timestamp.desc())
    
    for entry in entries:
        print(entry.timestamp , entry.content)

        option = input("Presione 'd' para eliminar y 'n' ir al siguiente")
        if(option == 'd'):
            print("Eliminando..")
            delete_entry(entry)
        elif(option == 'n'):
            next
        else:
            exit

def delete_entry(element):
    Entry.delete_instance(element)

def search_entries():
    view_entries(input('Selecciona un filtro'))

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries),
    ('d', delete_entry)
])

def menu_loop():
    choice = None

    while choice != 'q':
        print("Presione 'q' para salir ")
        for key,value in menu.items ():
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