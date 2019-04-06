from flask import (
     Flask, g, flash, redirect, render_template, request, session, url_for
)
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash

import models
import forms

from forms import MakeAppointment, RegisterForm, LoginForm

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


# @app.route('/reviews/<review_id>')
# def reviews(review_id = None):
#     if review_id == None:
#         reviews = models.Review.select().limit(10)
#         return render_template("reviews.html", reviews_template = reviews)
#     else:
#         review_id = int(review_id)
#         review = models.Reviews.get(models.Reviews.id == review_id)
#         return render_template("reviews.html", reviews=reviews)


@app.route('/profile', methods=['GET', 'POST'])
@app.route('/profile/', methods=['GET', 'POST'])
@app.route('/profile/<counselor_id>', methods=['GET', 'POST'])
def users(counselor_id = None):
    if counselor_id == None:
        user_id = int(current_user.id)
        user_data = models.User.get(models.User.id == user_id)
        return render_template("profile.html", user=user_data)
    else:
        counselor_id = int(counselor_id)
        user_data = models.User.get(models.User.id == counselor_id)
        return render_template("profile.html", user=user_data)

@app.route('/schedule/<counselor_id>',  methods=['GET', 'POST', 'DELETE'])
def get_schedule(counselor_id):
    counselorId = int(counselor_id)
    appointments = models.Appointment.select().where(models.Appointment.counselor == counselorId)
    return render_template("schedule.html", appointments=appointments)


@app.route('/appointments/<counselor_id>',  methods=['GET', 'POST', 'DELETE'])
#@app.route('/schedule', methods=['GET', 'POST'])
def schedule(counselor_id):
    #counselor_name = counselor_name
    counselor_id = int(counselor_id)
    #print(counselor_id)

    current_counselor = models.User.select().limit(10).where(models.User.id == counselor_id)[0]
    #print(counselor)

    #array of the appointments made by the user
    appointments = models.Appointment.select().limit(10).where(models.Appointment.client == current_user.id)

    counselors_for_appointments = []
    for i in appointments:
        counselor = models.User.select().where(models.User.id == i.counselor_id)
        #print(counselor.firstName)
        counselors_for_appointments.append(counselor)
        #print(i.counselor_id)

    
    print(counselors_for_appointments)
    print(appointments)

   

    # if a counselor wanted to see all the appointments a client made for them and who made them
    #if the counselor is signed in the code below will print out all appointment TIMES assigned to them
    #appointments = models.Appointment.select().limit(10).where(models.Appointment.counselor == current_user.id)
    #but who is the patient? /client?
    #client_email = models.User.select(email).where(models.Appointment.client_id == current_user.id)
    appointment_id = request.form.get('appointment_id', '')
    command = request.form.get('submit', '')

    #print(current_user.id)
    form = forms.MakeAppointment()
    if form.validate_on_submit():
        appointmentTaken = models.Appointment.get_or_none(models.Appointment.counselor == counselor_id and models.Appointment.date == form.date.data and models.Appointment.time == form.time.data)
        print(appointmentTaken)
    #if form.id.data == '': 
        # if !models.Appointment.select().where(models.Appointment.counselor == counselor_id and models.Appointment.date == form.date.data and models.Appointment.time == form.time.data)
        if appointmentTaken == None:
            models.Appointment.create_appointment(
                date=form.date.data, 
                time=form.time.data, 
                counselor = counselor_id,
                client = current_user.id
                )
            return redirect(url_for("schedule", counselor_id=counselor_id))
    if command == 'Delete':
            models.Appointment.delete_by_id(appointment_id)
            return redirect(url_for("schedule", counselor_id=counselor_id))
    # else:
    #     print("appt not valid?")
    return render_template("appointments.html", appointments_template=appointments, form=form, counselors=counselors_for_appointments, current_counselor=current_counselor)


@app.route('/all-therapists/', methods=['GET', 'POST'])
#@app.route('/schedule/<provider-username>', methods=['POST', 'GET']) (counselors)
def user():
    users = models.User.select().limit(10).where(models.User.isCounselor == 1)
    return render_template("therapists.html", users_template = users)


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

        return redirect(url_for('index'))
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