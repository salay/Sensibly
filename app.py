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


@app.route('/schedule/<counselor_id>',  methods=['GET', 'POST'])
#@app.route('/schedule', methods=['GET', 'POST'])
def schedule(counselor_id):
    #counselor_name = counselor_name
    counselorId = int(counselor_id)
    counselor_id = counselor_id
    #print(counselor_id)

    counselor = models.User.select().limit(10).where(models.User.id == counselor_id)[0]
    #print(counselor)

    appointments = models.Appointment.select().limit(10).where(models.Appointment.client == current_user.id)
    #print(appointments)

    # if a counselor wanted to see all the appointments a client made for them and who made them
    #if the counselor is signed in the code below will print out all appointment TIMES assigned to them
    #appointments = models.Appointment.select().limit(10).where(models.Appointment.counselor == current_user.id)
    #but who is the patient? /client?
    #client_email = models.User.select(email).where(models.Appointment.client_id == current_user.id)


    #print(current_user.id)
    form = forms.MakeAppointment()
    if form.validate_on_submit():
        #print("appt form valid?")
        #print('USER ID')
        #print(current_user.id)
        #if form.id.data == '': 
        models.Appointment.create_appointment(
            #date=form.date.data, 
            time=form.time.data, 
            counselor = counselorId,
            client = current_user.id
        )
        #return redirect('/schedule/<counselor_id>')
    else:
        print("appt not valid?")
    return render_template("appointments.html", appointments_template=appointments, form=form, counselor=counselor)


@app.route('/all-therapists/', methods=['GET', 'POST'])
#@app.route('/schedule/<provider-username>', methods=['POST', 'GET']) (counselors)
def user():
    users = models.User.select().limit(10).where(models.User.isCounselor == 1)
    return render_template("users.html", users_template = users)


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
            isCounselor=form.isCounselor.data
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
            isCounselor = False
            )
    except ValueError:
        pass
    app.run(debug=DEBUG, port=PORT)