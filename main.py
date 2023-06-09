"""
Sportsy
ICS4U
Emma Hong and Safa Sabry
This program is a web app created for coaches and players to have a multi-functional platform.
History:
November 1, 2022: Program creation and work
February 5, 2023: Continuing to use Kivy
February 26, 2023: Switch from app development to web development using Flask
March 25, 2023: Program creation and work
April 1, 2023: Jinja forms connected to Flask backend
April 16, 2023: Login system progress, CSS and navbar created
April 23, 2023: Database work
June 2, 2023: Work and program refining, completion
"""

from flask import Flask, render_template, url_for, request, flash, redirect, jsonify, session
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, DateField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
import sys
import os
import random
from werkzeug.security import generate_password_hash, check_password_hash
from form import *
from datetime import date, timedelta, datetime

# SQLite URI compatible - checking if OS is Windows or Linux/MacOS to make sure prefix is right
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

# app initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ics4u'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def generate_team_code():
    code = random.randint(100000, 999999)
    print(code)
    return code

# initializing database and login manager
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# initializing User database table
class User(db.Model, UserMixin):
    
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    fname=db.Column(db.String(20))
    lname=db.Column(db.String(20))
    email=db.Column(db.String(20))
    password_hash=db.Column(db.String(128))
    dob = db.Column(db.Date)
    pb = db.Column(db.String(20))
    healthinfo=db.Column(db.String(100))
    dom_side = db.Column(db.String(5))
    coach_or_player=db.Column(db.String(6))
    team_code = db.Column(db.Integer)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password) 

# initializing log database table
class HealthLog(db.Model):
    __tablename__="healthlog"
    log_id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    id=db.Column(db.Integer)
    log=db.Column(db.String(1000))

# initializing login manager and user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=('GET', 'POST'))
def index():    

    # if the user is not logged in, redirect to the login page
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
       
    return render_template('index.html')

@app.route('/profile')
def profile():
    
    # if the user is not logged in, redirect to the login page
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('profile.html')
  
@app.route('/calendar', methods = ['GET','POST'])
#to do: add events to db, allow user to save events to list then add to database, allow user to add an event for another month) 
def calendar():
    
    # if the user is not logged in, redirect to the login page
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
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

@app.route('/roster', methods = ['GET','POST'])
def roster():
    
    form=CodeReceiver()
    if current_user.team_code == None and current_user.coach_or_player == 'coach':
        current_user.team_code = generate_team_code()  
        db.session.commit()
   

    elif current_user.team_code == None and current_user.coach_or_player == 'player': 
        users=None
    
    if request.method=="POST" and form.validate_on_submit():
        code=form.code.data
        
        if current_user.coach_or_player == 'player':
            current_user.team_code=code
            db.session.commit()

            users = User.query.filter_by(team_code=current_user.team_code).all() 
        
        return redirect(url_for('roster'))
    
    # if the user is not logged in, redirect to the login page
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    users = User.query.filter_by(team_code=current_user.team_code).all()
    return render_template('roster.html', form=form, users=users)

@app.route('/login', methods=["GET", "POST"])
def login():
    session.pop('_flashes', None)
    form = LoginForm() 

    # if a "POST" request is sent and the form has been validated
    if request.method == "POST" and form.validate_on_submit():
        
        # initializing data from the form
        email = form.login_email.data
        password = form.login_password.data

        # identifying user in database
        user = User.query.filter_by(email=email).first()


        # checking if user is valid and logging user in
        if user and user.validate_password(password):
            login_user(user)
            if current_user.team_code == None and current_user.coach_or_player == 'coach':
                current_user.team_code = generate_team_code()
                db.session.commit()
                print(current_user.team_code)
            
            return redirect(url_for('profile'))
        
        # flash invalid message
        else:
            flash('invalid email or password!', 'error')

    return render_template('login.html', form=form)
        

@app.route('/signup', methods=["GET", "POST"])
def signup():
    
    # initialize form
    form = SignupForm()
    
    # if there is a "POST" request and form is validated
    if request.method=="POST" and form.validate_on_submit():
        # getting data from the form submission
        fname=form.fname.data
        lname=form.lname.data
        email=form.email.data
        password=form.password.data
        dob=form.dob.data
        pb=form.pb.data
        healthinfo=form.healthinfo.data
        right=form.right.data
        left=form.left.data
        coach=form.coach.data
        player=form.player.data
        dom_side=' '
        coach_or_player='coach'
        
        # depending on boolean returned, assign value to dominant side
        if right:
            dom_side = 'right'
        elif left:
            dom_side='left'   
        
        # depending on boolean returned, assign value to whether user is coach or player and generate code
        if coach:
            coach_or_player = 'coach'
            user = User(fname=fname, lname=lname, email=email, dob=dob,pb=pb, healthinfo=healthinfo, dom_side=dom_side, coach_or_player=coach_or_player, team_code=generate_team_code())
            user.set_password(password)
        elif player:
            coach_or_player='player'  
            user = User(fname=fname, lname=lname, email=email, dob=dob,pb=pb, healthinfo=healthinfo, dom_side=dom_side, coach_or_player=coach_or_player)
        
        user.set_password(password) 
        
        # initialize user using data and set password
        
        
        
        # add user to database session and commit changes
        db.session.add(user)
        db.session.commit()
                
        # redirect to home page after login
        return redirect(url_for('index'))
    
    return render_template('signup.html', form=form)

@app.route('/log', methods=["GET", "POST"])
def log():  
    
    # initialize form and date
    form = HealthLogForm()
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
        
    # if there is a "POST" request
    if request.method=="POST":
        
        # getting recorded log
        log = form.log.data

        # identifying current user id
        id= current_user.id
        
        # creating health log
        log_entry = HealthLog(id=id, log=log)
        
        # add log entry to database session and commit changes
        db.session.add(log_entry)
        db.session.commit()

        return redirect(url_for('log'))
    
    # if the user is not logged in, redirect to the login page
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    log_data = HealthLog.query.filter_by(id=current_user.id).all()
    return render_template('log.html', form=form, log_data=log_data, year=year, month=month, day=day)

@app.route('/logout')
@login_required
def logout():
    
    # logging out the user and clearing messages
    logout_user()
    session.pop('_flashes', None)    
    return render_template('logout.html')


@app.errorhandler(Exception)
def handle_error(e):
    # returning the error to the screen
    return 'An error occurred: ' + str(e), 500
  
if __name__ == "__main__":
    with app.app_context():
        # creating all databases that were initialized and running web app
        db.create_all()
        
    app.run(debug=True, port=5000)
