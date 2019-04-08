import datetime
import moment
from flask_moment import Moment
from peewee import *

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('sensibly.db')

class User(UserMixin, Model):
    firstName = CharField()
    lastName = CharField()
    email = CharField(unique=True)
    password = CharField(max_length=100)

    phone = IntegerField(default=1234567)
    address = CharField()
    city = CharField()
    state = CharField()
    zipcode = IntegerField(default=00000)
    #role = CharField()
    picture = TextField(default="http://www.mentalhealthresourcespc.com/faces.jpg")
    isCounselor = BooleanField(default="False")
    joined_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)

    @classmethod
    def create_user(cls, firstName, lastName, phone, address, city, state, zipcode, picture, email, isCounselor, password):
        try:
            cls.create(
                firstName=firstName,
                lastName=lastName,
                phone = phone,
                address = address,
                city = city,
                state = state,
                zipcode = zipcode,
                picture = picture,
                email=email,
                isCounselor=isCounselor,
                password=generate_password_hash(password)
                )
        except IntegrityError:
            raise ValueError("User already exists")

class Appointment(Model):
    counselor = ForeignKeyField(model=User)
    client = ForeignKeyField(model=User)
    date = DateTimeField()
    time = CharField()
    #time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

    @classmethod
    def create_appointment(cls, counselor, client, date, time):
        try:
            cls.create(
                counselor=counselor,
                client=client,
                date=date,
                time=time
            )
        except IntegrityError:
            raise

            
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Appointment], safe=True)
    DATABASE.close()
