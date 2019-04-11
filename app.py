from flask import (
     Flask, g, flash, redirect, render_template, request, session, url_for
)
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash

import models
import forms

import datetime

from forms import MakeAppointment, RegisterForm, LoginForm, EditProfileForm

app = Flask(__name__)
app.secret_key = 'watermelon.watermelon.watermelon'

DEBUG = True
PORT = 8000

login_manager = LoginManager()
## sets up our login for the app
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

@app.route('/')
def index():
    return render_template("home.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.route('/my-profile', methods=['GET', 'POST'])
@app.route('/my-profile/', methods=['GET', 'POST'])
def profile():
    user_id = int(current_user.id)
    user_data = models.User.get(models.User.id == user_id)
    form = EditProfileForm()
    appointments = models.Appointment.select().where(models.Appointment.client == current_user.id)

    command = request.form.get('submit', '')
    if command == 'Edit Profile':
        user = models.User.get(models.User.id == user_id)
        user.firstName = form.firstName.data
        user.lastName = form.lastName.data
        user.phone = form.phone.data
        user.address = form.address.data
        user.city = form.city.data
        user.state = form.state.data
        user.zipcode = form.zipcode.data
        user.picture = form.picture.data
        user.save()
        return redirect('/my-profile')

    return render_template("edit_profile.html", user=user_data, form=form, appointments_template= appointments)



@app.route('/schedule/',  methods=['GET', 'POST', 'DELETE'])
def get_schedule():
    counselor_id = int(current_user.id)

    # if the counselor is signed in the code below will print out all appointments assigned to them and the times and who made them
    appointments = models.Appointment.select().where(models.Appointment.counselor == counselor_id).order_by(models.Appointment.date.asc())
    form = forms.MakeAppointment()
    #unfortunately if appointments is null the counselor gets an error on the page
    appointment_id = request.form.get('appointment_id', '')
    command = request.form.get('submit', '')
    if command == 'Delete':
        models.Appointment.delete_by_id(appointment_id)
        return redirect(url_for("get_schedule", appointments=appointments, counselor_id=counselor_id))
    return render_template("schedule.html", appointments=appointments, form=form)



@app.route('/schedule/<counselor_id>/edit',  methods=['GET', 'POST', 'DELETE'])
def edit(counselor_id):
    counselor_id = int(counselor_id)
    current_counselor = models.User.select().where(models.User.id == counselor_id)[0]
    #array of the appointments made by the user
    appointments = models.Appointment.select().where(models.Appointment.client == current_user.id)
    appointment_id = request.form.get('appointment_id', '')
    command = request.form.get('submit', '')

    form= forms.MakeAppointment()

    if form.validate_on_submit:
        print("hey I'm editing yay!")
        print(appointment_id)
        appointment_id = int(appointment_id)
        appointment = models.Appointment.get(models.Appointment.id == appointment_id)
        
        appointment.date = form.date.data
        print(form.date.data)
        appointment.time = form.time.data
        print(form.time.data)
        counselor_id = appointment.counselor_id
        current_user.id = appointment.client.id    
        appointment.save()
        return redirect(url_for("get_schedule", counselor_id=counselor_id))

    return render_template("appointments.html", appointments_template=appointments, form=form, current_counselor=current_counselor, counselor_id=counselor_id)



@app.route('/appointments/<counselor_id>/edit',  methods=['GET', 'POST', 'DELETE'])
def edit_appointment(counselor_id):
    counselor_id = int(counselor_id)
    current_counselor = models.User.select().where(models.User.id == counselor_id)[0]
    #array of the appointments made by the user
    appointments = models.Appointment.select().where(models.Appointment.client == current_user.id)
    appointment_id = request.form.get('appointment_id', '')
    command = request.form.get('submit', '')

    form= forms.MakeAppointment()

    if form.validate_on_submit:
        print("hey I'm editing yay!")
        print(appointment_id)
        appointment_id = int(appointment_id)
        appointment = models.Appointment.get(models.Appointment.id == appointment_id)
        
        appointment.date = form.date.data
        print(form.date.data)
        appointment.time = form.time.data
        print(form.time.data)
        counselor_id = appointment.counselor_id
        current_user.id = appointment.client.id    
        appointment.save()
        return redirect(url_for("schedule", counselor_id=counselor_id))

    return render_template("appointments.html", appointments_template=appointments, form=form, current_counselor=current_counselor, counselor_id=counselor_id)



@app.route('/appointments/<counselor_id>',  methods=['GET', 'POST', 'DELETE'])
def schedule(counselor_id):
    counselor_id = int(counselor_id)

    current_counselor = models.User.select().where(models.User.id == counselor_id)[0]

    #array of the appointments made by the user
    appointments = models.Appointment.select().where(models.Appointment.client == current_user.id)

    counselors_for_appointments = []
    for i in appointments:
        counselor = models.User.select().where(models.User.id == i.counselor_id)
        counselors_for_appointments.append(counselor)

    appointment_id = request.form.get('appointment_id', '')
    command = request.form.get('submit', '')
    form = forms.MakeAppointment()

#deletes an appointment
    if command == 'Cancel':
        models.Appointment.delete_by_id(appointment_id)
        return redirect(url_for("schedule", counselor_id=counselor_id))

#creates a new appointment
    if form.validate_on_submit():
        #cannot create appointment in the past
        if form.date.data > datetime.date.today():
            print("I'm creating an appt")
            appointmentTaken = models.Appointment.select().where(
                (models.Appointment.counselor == counselor_id) &
                (models.Appointment.date == form.date.data) &
                (models.Appointment.time == form.time.data)
                )
            #print(appointmentTaken)


        # why doesn't this work: if !models.Appointment.select().where(models.Appointment.counselor == counselor_id and models.Appointment.date == form.date.data and models.Appointment.time == form.time.data)
        # code below checks to see if appoitnment is taken
            if appointmentTaken.count() == 0:
                flash("Created New Appointment.","success")
                models.Appointment.create_appointment(
                    date=form.date.data, 
                    time=form.time.data, 
                    counselor = counselor_id,
                    client = current_user.id
                    )
                return redirect(url_for("schedule", counselor_id=counselor_id))
        else:
            flash("Appoinment slot already taken.","error")
            return redirect(url_for("schedule", counselor_id=counselor_id))

    return render_template("appointments.html", appointments_template=appointments, form=form, counselors=counselors_for_appointments, current_counselor=current_counselor)



@app.route('/all-therapists/', methods=['GET', 'POST'])
#@app.route('/schedule/<provider-username>', methods=['POST', 'GET']) (counselors)
def therapists():
    therapists = models.User.select().where(models.User.isCounselor == 1)
    return render_template("therapists.html", therapists_template = therapists)



@app.route('/therapist-profile/<counselor_id>', methods=['GET', 'POST'])
def therapistProfile(counselor_id = " "):
        counselor_id = int(counselor_id)
        user_data = models.User.get(models.User.id == counselor_id)
        return render_template("therapist_profile.html", user=user_data, counselor_id = counselor_id)



@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        print("form valid?")
        flash('Yay you registered', 'success')
        models.User.create_user(
            firstName=form.firstName.data,
            lastName=form.lastName.data,
            email=form.email.data,
            password=form.password.data,
            isCounselor=form.isCounselor.data,
            phone = form.phone.data,
            address = form.address.data,
            city = form.city.data,
            state = form.state.data,
            zipcode = form.zipcode.data,
            picture = form.picture.data,
            )

        return redirect(url_for('login'))
    print("not valid?")
    return render_template('register.html', form=form)



@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("your email or password doesn't match", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                ## creates session
                login_user(user)
                flash("You've been logged in", "success")
                return redirect(url_for('index'))
            else:
                flash("your email or password doesn't match", "error")
    return render_template('login.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out", "success")
    return redirect(url_for('index'))


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            firstName="Jiminy",
            lastName="Bob",
            email="jim@jim.com",
            password='password',
            isCounselor = False,
            phone = 1234567,
            address = "123 Nowhere Dr.",
            city = "Nowhere",
            state = "MT",
            zipcode = 12345,
            picture = " ",
            )
    except ValueError:
        pass
    app.run(debug=DEBUG, port=PORT)