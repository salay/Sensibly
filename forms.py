from flask_wtf import FlaskForm as Form

import datetime
from models import User

from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SelectField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                               Length, EqualTo)

from wtforms.fields.html5 import DateField

def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')

class RegisterForm(Form):
    firstName = StringField(
        'First Name',
        validators=[
            DataRequired()
        ])
    lastName = StringField(
        'Last Name',
        validators=[
            DataRequired()
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=4, message='Minimum password length is 4 characters'),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )
    isCounselor = BooleanField(
        'Are you a counselor?',
    ) 

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class MakeAppointment(Form):
    #date = DateField('The date', default=datetime.datetime.now)
    time = SelectField(u"Which Time ", choices=[('9:00 AM', '10:00 AM'), ('10:00 AM', '11:00 AM'), 
    ('11:00 AM', '12:00 PM'), ('12:00 PM', '1:00 PM'), ('1:00 PM', '2:00 PM'), ('2:00 PM', '3:00 PM'), 
    ('3:00 PM', '4:00 PM'), ('4:00 PM', '5:00 PM') ])
                