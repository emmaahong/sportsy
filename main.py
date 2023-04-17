from flask import Flask, render_template, url_for, request, flash, redirect
import sqlite3
from sqlite3 import Error

# ...

app = Flask(__name__)



global names
name_message = { 'message' : 'Welcome to Sportsy',
          'firstname' :'' }

names = [name_message]

@app.route('/', methods=('GET', 'POST'))
def index():
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

@app.route('/roster')
def roster():
    if request.method == "POST":
        injuries = request.form.get("injuries")
        return render_template('roster.html')
    return render_template('roster.html')
    
if __name__ == "__main__":
  app.run(debug=True, port=5000)
