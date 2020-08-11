import datetime
from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

db = SqliteDatabase("database.sql")

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=120)
    joined_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        order_by = ('-joined_at',)

    def get_posts(self):
        return Post.select().where(Post.user == self)

    @classmethod
    def create_user(self, username, email, password):
        try:    
            self.create(
                username = username,
                email = email,
                password = generate_password_hash(password)
            )
        except:
            raise ValueError('User already exists')

class Post(Model):
    
    user = ForeignKeyField(
        User,
        related_name='posts',
    )
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        order_by = ('-joined_at',)


def initialize():
    db.connect()
    db.create_tables([User], safe=True)
    db.close()