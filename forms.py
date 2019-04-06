from flask_wtf import FlaskForm as Form

import datetime
from models import User

from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SelectField, DateTimeField, IntegerField
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
    
    phone = IntegerField('Phone Number')
    address = StringField('Address')
    city = StringField('City')

    state = SelectField(u"Which State ",
        choices=[
            ('None', 'State (if applicable)'),
            ('AL', 'Alabama'),
            ('AK', 'Alaska'),
            ('AZ', 'Arizona'),
            ('AR', 'Arkansas'),
            ('CA', 'California'),
            ('CO', 'Colorado'),
            ('CT', 'Connecticut'),
            ('DE', 'Delaware'),
            ('DC', 'District of Columbia'),
            ('FL', 'Florida'),
            ('GA', 'Georgia'),
            ('HI', 'Hawaii'),
            ('ID', 'Idaho'),
            ('IL', 'Illinois'),
            ('IN', 'Indiana'),
            ('IA', 'Iowa'),
            ('KS', 'Kansas'),
            ('KY', 'Kentucky'),
            ('LA', 'Louisiana'),
            ('ME', 'Maine'),
            ('MD', 'Maryland'),
            ('MA', 'Massachusetts'),
            ('MI', 'Michigan'),
            ('MN', 'Minnesota'),
            ('MS', 'Mississippi'),
            ('MO', 'Missouri'),
            ('MT', 'Montana'),
            ('NE', 'Nebraska'),
            ('NV', 'Nevada'),
            ('NH', 'New Hampshire'),
            ('NJ', 'New Jersey'),
            ('NM', 'New Mexico'),
            ('NY', 'New York'),
            ('NC', 'North Carolina'),
            ('ND', 'North Dakota'),
            ('OH', 'Ohio'),
            ('OK', 'Oklahoma'),
            ('OR', 'Oregon'),
            ('PA', 'Pennsylvania'),
            ('RI', 'Rhode Island'),
            ('SC', 'South Carolina'),
            ('SD', 'South Dakota'),
            ('TN', 'Tennessee'),
            ('TX', 'Texas'),
            ('UT', 'Utah'),
            ('VT', 'Vermont'),
            ('VA', 'Virginia'),
            ('WA', 'Washington'),
            ('WV', 'West Virginia'),
            ('WI', 'Wisconsin'),
            ('WY', 'Wyoming'),
            ])

    zipcode = IntegerField('Zipcode')
    picture = StringField('Picture')

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
    date = DateField('The date', default=datetime.datetime.now, validators=[DataRequired()])
    time = SelectField(u"Which Time ", choices=[('9:00 AM - 10:00 AM', '9:00 AM - 10:00 AM'), ('10:00 AM - 11:00 AM', '10:00 AM - 11:00 AM'), 
    ('11:00 AM - 12:00 PM', '11:00 AM - 12:00 PM'), ('12:00 PM - 1:00 PM', '12:00 PM - 1:00 PM'), ('1:00 PM - 2:00 PM', '1:00 PM - 2:00 PM'), ('2:00 PM - 3:00 PM', '2:00 PM - 3:00 PM'), 
    ('3:00 PM - 4:00 PM', '3:00 PM - 4:00 PM'), ('4:00 PM - 5:00 PM', '4:00 PM - 5:00 PM') ])


    # class MyForm(forms.Form):
    # date = forms.DateField(...)

    # def clean_date(self):
    #     date = self.cleaned_data['date']
    #     if date < datetime.date.today():
    #         raise forms.ValidationError("The date cannot be in the past!")
    #     return date