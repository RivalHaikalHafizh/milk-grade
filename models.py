import datetime
from peewee import *

DATABASE =SqliteDatabase('Milk.db')

class BaseModel(Model):
    class Meta:
        database =DATABASE

class User(BaseModel):
    username=CharField(unique=True)
    password=CharField()

class Message(BaseModel):
    # user_id=ForeignKeyField(User,backref='messages')
    content =TextField()
    published_at=DateTimeField(default=datetime.datetime.now())


class MilkGrade(BaseModel):
    Temprature=IntegerField()
    Odor=IntegerField()
    Fat =IntegerField()
    Turbidity=IntegerField()
    Grade=CharField()


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([MilkGrade,User,Message],safe=True)
    DATABASE.close()