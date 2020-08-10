from peewee import *

db = SqliteDatabase('students.db')

class Student(Model):
    username = CharField(max_length=255, unique=True)
    points = IntegerField(default=0)

    class Meta:
        database = db

students = [
    {'username': 'Daniel',
    'points': 444},
    {'username': 'Aaron',
    'points': 555},
    {'username': 'Lain',
    'points': 666}
]

def add_students():
    for student in students:
        try:
            Student.create(username=student['username'],
                       points=student['points'])
        except IntegrityError:
            student_record = Student.get(username=student['username'])
            student_record.points = student['points']
            student_record.save()         

if __name__ == "__main__":
    db.connect()
    db.create_tables([Student], safe=True)
    add_students()