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
  
@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

conn = None
cursor = None

@app.route('/calendar-events')
def calendar_events():

	try:
		conn = sqlite3.connect()
		cursor = conn.cursor(sqlite3.cursors.DictCursor)
		cursor.execute("SELECT id, title, url, class, UNIX_TIMESTAMP(start_date)*1000 as start, UNIX_TIMESTAMP(end_date)*1000 as end FROM event")
		rows = cursor.fetchall()
		resp = jsonify({'success' : 1, 'result' : rows})
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

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
    with app.app_context():    
        db.create_all()
    app.run(debug=True, port=5000)
