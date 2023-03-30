from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
  
@app.route('/profile')
def profile():
    return render_template('profile.html')
  
@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/roster')
def roster():
    return render_template('roster.html')
    
if __name__ == "__main__":
  app.run(debug=True, port=5000)
