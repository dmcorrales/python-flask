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

    def get_stream(self):
        return Post.select().where(Post.user == self)

    def following(self):
        return(
            User.select().join(
                Relationship, on=Relationship.to_user
            ).where(
                Relationship.from_user == self   
            )
        )

    def followers(self):
        return(
            User.select().join(
                Relationship, on=Relationship.from_user
            ).where(
                Relationship.to_user == self   
            )
        )  

    @classmethod
    def create_user(self, username, email, password):
        try:
            with db.transaction():    
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


class Relationship(Model):
    from_user = ForeignKeyField(User, related_name='relationships')
    to_user = ForeignKeyField(User, related_name='related_to')

    class Meta:
        database = db
        indexes = (
            (('form_user', 'to_user'), True)
        )

def initialize():
    db.connect()
    db.create_tables([User, Post], safe=True)
    db.close()