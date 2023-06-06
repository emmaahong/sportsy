from flask import Flask, render_template, url_for, request, flash, redirect, jsonify
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
# from init_db import add_text
import sys
import os
from werkzeug.security import generate_password_hash, check_password_hash
from form import *
from datetime import date, timedelta

# app initialization
# SQLite URI compatible - checking if OS is Windows or Linux/MacOS to make sure prefix is right
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

# app initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ics4u'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initializing database
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# initializing User class
class User(db.Model, UserMixin):
    
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    fname=db.Column(db.String(20))
    lname=db.Column(db.String(20))
    email=db.Column(db.String(20))
    password_hash=db.Column(db.String(128))
    dob = db.Column(db.Date)
    pb = db.Column(db.String(20))
    healthinfo=db.Column(db.String(20))
    dom_side = db.Column(db.String(5))
     
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password) 

# initializing login manager and user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=('GET', 'POST'))
def index():
    print("in the index fnc")
    
    print(current_user.is_authenticated)
    if not current_user.is_authenticated:
        print('not authenticated...?')
        return redirect(url_for('login'))
    
    if request.method == "POST":
        print("in the post if/else")
        
        
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')
  
@app.route('/calendar', methods = ['GET','POST'])
#to do: add events to db, allow user to save events to list then add to database, allow user to add an event for another month) 
def calendar():
    #calendar info 
    today = str(date.today())
    calendar_info = today.split("-")
    num_month = int(calendar_info[1])
    year = calendar_info[0]
    first_day_of_month = (date.today().replace(day=1)).weekday()

    #finding number of days in the month (28,29,30, or 31)
    if num_month == 4 or 6 or 9 or 11:
        last_day_of_month = 30
    elif num_month == 2:
        if year == 2000 and year % 400 == 0:
            last_day_of_month = 29
        elif year % 4 == 0:
            last_day_of_month = 29
        else:
            last_day_of_month = 28
    else: 
        last_day_of_month = 31

    #creating list of days for printing calendar display 
    days = []
    for x in range(first_day_of_month):
        days.append(" ")
    for i in range(last_day_of_month):
        days.append(i+1)
    for y in range(35 - last_day_of_month):
        days.append(" ")  
        
    #more lists for printing 
    all_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    all_events = ["-"]*35
    all_events[6]= ["this is an example of an event"]
    str_month = all_months[num_month-1]

    #Textbox for adding events 
    if request.method == 'POST':
        user_date = request.form.get('date')
        time = request.form.get('time')
        place = request.form.get('place')
        name = request.form.get('name')
        extra_info = request.form.get('extra_info')

        # Store the information in a list
        information = [name, user_date, time, place, extra_info]
        # print(information)
        # Do something with the information
        print(information)
        list_user_date_of_event = user_date.split("-")
        user_month_of_event = list_user_date_of_event[1]
        print(num_month)
        print(user_month_of_event)
        if int(user_month_of_event) == int(num_month):
            all_events[6] = information
        else:
            print("error")
        print(all_events)
        return render_template('success.html', information = information )
    # return render_template('success.html', )

    # return render_template('form.html')
    return render_template('calendar.html', year = year, month = str_month, days = days, today = today, events=all_events)

conn = None
cursor = None

@app.route('/roster')
def roster():
    return render_template('roster.html', rostername = "yo name")

#adding textbox to roster
@app.route("/add_text", methods=["POST","GET"])
def addText():
    if request.method == "POST":
        text_value = request.form["textv"]
        #saving to database
        add_new = add_text(text_value)
        return redirect(url_for('name'))
    else:
        return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()


    if request.method == "POST" and form.validate_on_submit():
        email = form.login_email.data
        password = form.login_password.data

        user = User.query.filter_by(email=email).first()

        if user and user.validate_password(password):
            login_user(user)
            flash('you are logged in!', 'success')
            next = request.args.get('next')
            
            if not url_has_allowed_host_and_scheme(next, request.host):
                return abort(400)
            
            return redirect(url_for('profile'))
        
        else:
            flash('invalid email or password!', 'error')

    return render_template('login.html', form=form)
        

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if request.method=="POST" and form.validate_on_submit():
        fname=form.fname.data
        lname=form.lname.data
        email=form.email.data
        password=form.password.data
        confirm_password = form.confirm_password.data
        dob=form.dob.data
        pb=form.pb.data
        healthinfo=form.healthinfo.data
        right=form.right.data
        left=form.left.data
        dom_side=' '
        
        if right:
            dom_side = 'right'
        elif left:
            dom_side='left'     
        
        print(dom_side)
        
        user = User(fname=fname, lname=lname, email=email, dob=dob,pb=pb, healthinfo=healthinfo, dom_side=dom_side)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        print('yay'+user.fname+'is logged in....')
        
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route('/log')
def log():
    return render_template('log.html')

@app.route('/playerorcoach')
def player_or_coach():
    return render_template('playerorcoach.html')

@app.route('/coachsignup')
def coach_signup():
    return render_template('coach_signup.html')

@app.route('/playersignup')
def player_signup():
    return render_template('player_signup.html')

@app.errorhandler(Exception)
def handle_error(e):
    return 'An error occurred: ' + str(e), 500
  
if __name__ == "__main__":
<<<<<<< HEAD
    with app.app_context():
=======
    with app.app_context():    
>>>>>>> 9a24a6277441c4a5ad0ca009ab7549acfbfbda51
        db.create_all()
    app.run(debug=True, port=5000)
