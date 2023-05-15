from flask import Flask, render_template, url_for, request, flash, redirect, jsonify
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_wtf import FlaskForm
from init_db import add_text
import sys
import os
from werkzeug.security import generate_password_hash, check_password_hash

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

conn = sqlite3.connect('database_name.db')
c = conn.cursor()
c.execute('SELECT * FROM users')
rows = c.fetchall()
for row in rows:
    print(row)
conn.close()

# app initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ics4u'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# database initialization
# db=SQLAlchemy(app)
conn=sqlite3.connect('database.db')
cursor = conn.cursor()
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

class User(db.Model, UserMixin):
    def __init__(self):
        id=db.Column(db.Integer, primary_key=True,autoincrement=True)
        fname=db.Column(db.String(20))
        lname=db.Column(db.String(20))
        email=db.Column(db.String(20))
        password_hash=db.Column(db.String(128))
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(self.password_hash)
    
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password) 

# welcome message
global names
name_message = { 'message' : 'Welcome to Sportsy',
          'firstname' :'' }

names = [name_message]

# @app.route('/', methods=('GET', 'POST'))
# def index():
#     conn = get_db_connection()
#     username = conn.execute('SELECT * FROM users').fetchall()
#     conn.close()
#     if request.method == "POST":
#         fname = request.form.get("firstname")
#         name_message['firstname'] = str(fname)
#         return render_template('index.html',  names = names)
#     users = load_user(0)
#     return render_template('index.html',  names = names, users=users)
  

@app.route('/', methods=('GET', 'POST'))
def index():
    # conn = get_db_connection()
    # username = conn.execute('SELECT * FROM users').fetchall()
    # conn.close()
    if request.method == "POST":
        
        irstfname = request.form.get("firstname")
        name_message['firstname'] = str(irstfname)
        return render_template('index.html',  names = names)
    return render_template('index.html',  names = names)

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
    

@app.route('/login')
def login():
    # form = LoginForm()
    # if form.validate_on_submit():
    #     login_user(user) 
    
    return render_template('login.html')

@app.route('/signup')
def signup():
    # form = LoginForm()
    # if form.validate_on_submit():
    #     login_user(user) 
    
    return render_template('signup.html')

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
    
if __name__ == "__main__":
  app.run(debug=True, port=5000)
