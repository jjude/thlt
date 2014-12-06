from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired,URL, Email

class signupForm(Form):
  email = StringField("Email", validators=[DataRequired(message='You need to enter email'), Email(message="Enter a valid email address")])
  password = StringField("OTP Code", validators=[DataRequired(message='You need to enter password')])
  submit = SubmitField("Sign Up")
