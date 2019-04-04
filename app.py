from flask import (
     Flask, g, flash, redirect, render_template, request, session, url_for
)
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash

import models
import forms

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


@app.route('/users/', methods=['GET'])
# @app.route('/schedule/', methods=['GET'])
#@app.route('/schedule/<provider-username>', methods=['POST', 'GET'])
def schedule():
    users = models.User.select().limit(10)
    return render_template("users.html", users_template = users)


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash('Yay you registered', 'success')
        models.User.create_user(
            email=form.email.data,
            password=form.password.data
            )

        return redirect(url_for('index'))
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
            email="jim@jim.com",
            password='password'
            )
    except ValueError:
        pass
    app.run(debug=DEBUG, port=PORT)