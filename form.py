from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class SignupForm(FlaskForm):
    fname = StringField('first name', validators=[DataRequired()])
    lname = StringField('last name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm Password', validators=[DataRequired(), EqualTo('password')])
    dob = DateField('date of birth', validators=[DataRequired()])
    pb = TextAreaField('personal bests')
    healthinfo = TextAreaField('health information')
    right = BooleanField('right')
    left = BooleanField('left')
    submit = SubmitField('sign up')

class LoginForm(FlaskForm):
    login_email = StringField('email', validators=[DataRequired(), Email()])
    login_password = PasswordField('password', validators=[DataRequired()])
    login_submit = SubmitField('sign up')

