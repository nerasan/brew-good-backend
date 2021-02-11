from peewee import *
from flask_login import UserMixin
import datetime

DATABASE = PostgresqlDatabase('brew_good_app', host='localhost', port=5432)

# without class Meta inside the User Model - the User Model will not link to the database. this is what creates the relationship between user model and database.
# since we are including this in every single model, we are making it here.
class BaseModel(Model):
    class Meta:
        database = DATABASE

# inherit from BaseModel rather than Model, so the class Meta is built into the class
class User(UserMixin, BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

class Person(BaseModel):
    city = CharField()
    country = CharField()
    about = TextField()

# most of this will be pulled from Yelp API so does there need to be a model?
class Cafe(BaseModel):
    name = CharField()
    address = CharField()
    city = CharField()
    country = CharField()
    description = CharField()
    rating = CharField()
    # created_at = DateTimeField(default=datetime.datetime.now)

# through table only if we have many-to-many. if one-to-many, that is defined within that Model. for example `owner = ForeignKeyField` in `Dog` model
# many to many - a user can have many cafes favorited and a cafe can have many users
class UserCafe(BaseModel):
    user = ForeignKeyField(User, backref='users')
    cafe = ForeignKeyField(Cafe, backref='cafe')

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Person, Cafe, UserCafe], safe=True)
    print("tables created")
    DATABASE.close()