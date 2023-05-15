from flask import Flask, render_template, url_for, request, flash, redirect, jsonify
import sqlite3
from sqlite3 import Error
# from flask_wtf import FlaskForm
from init_db import add_text

# from flask_login import (
#     UserMixin,
#     login_user,
#     LoginManager,
#     current_user,
#     logout_user,
#     login_required,
# )

# app initialization
app = Flask(__name__)

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
        fname = request.form.get("firstname")
        name_message['firstname'] = str(fname)
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
    
if __name__ == "__main__":
  app.run(debug=True, port=5000)
