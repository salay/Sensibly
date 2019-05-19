# Sensibly

An Acuity-like scheduling app for therapists....
(that might've devolved into an app to schedule time with therapy dogs).

Deployed here: https://sensibly-capstone.herokuapp.com/

## Technologies Used: 
- [Python](https://www.python.org/)
- [WTForms](https://wtforms.readthedocs.io/en/stable/)
- [Flask](http://flask.pocoo.org/docs/1.0/)
- [Jinja](http://jinja.pocoo.org/)
- [SQLite](https://www.sqlite.org/index.html)
- [PostgreSQL](https://www.postgresql.org/)
- [Vanilla JS]()
- [Bootstrap](https://getbootstrap.com/)

## Features:
Flask Authentication with Validation (Register for Account and Login)

Flexible Search Bar

User Profile Page

Accessibility was restricted when users were not signed in OR if users were not counselors:
- Could not create appointments if not signed in.
- If signed in as a user, you couldn't view a schedule of appointments (because you don't have one).
- Cannot schedule appointments with non-counselors or view client profiles. 
- Cannot view anyone's personal profile or therapist's schedule other than your own.

Appointments Page has full CRUD:  
User can click on a date, make an appointment, view that appointment on the same page, edit the appointment, and delete the apointment

### Wins
- Flask auth Worked on Day 2 of this project.
- Making a calendar!
- 404 page was so easy to put in place.

### Challenges
- Making a Calendar.
- Edit functionality for appointments. 
- Working in Modals.
- all-therapists route is slow. I don't know why yet.

#### Shoutouts
Thank you stackoverflow and all the WDI instructors.  
Matt (help with calendar & scheduling)  
Heggy (error messages, wireframes & deployment), Tiffany (edit), Nassima (setting up models), Amberly (postgres migration)   

#### Code I'm proud of:

Appointments cannot be scheduled in the past on neither the frontend, nor the backend.
Appointments cannot be duplicated.

![Screenshot ](../master/Sensibly-app.png)

Edit Functionality for App.py is on separate route to make it work.
![Screenshot ](../master/Sensibly-app.py-edit.png)


