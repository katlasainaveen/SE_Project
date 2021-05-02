from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField
from wtforms_components import TimeField


class LoginForm(FlaskForm):
    login_type = RadioField("login as: ", choices=["Warden", "Student"], default="Student")
    username = StringField("Username(Roll Number)", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ResetPasswordStudent(FlaskForm):
    roll_number = StringField("Roll number", validators=[DataRequired()])
    old_password = PasswordField("Old Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class NewStudent(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    roll_number = StringField("Roll Number", validators=[DataRequired()])
    phone_number = StringField("Phone Number", validators=[DataRequired()])
    parents_number = StringField("Parent's Phone Number", validators=[DataRequired()])
    year_section = StringField("Year and Section", validators=[DataRequired()])
    department = StringField("Department", validators=[DataRequired()])
    password = PasswordField("Add Password", validators=[DataRequired()])
    submit = SubmitField("Add Student")


class NewWarden(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    roll_number = StringField("Roll Number", validators=[DataRequired()])
    phone_number = StringField("Phone Number", validators=[DataRequired()])
    password = PasswordField("Add Password", validators=[DataRequired()])
    submit = SubmitField("Add Warden")


class RegisterGatepass(FlaskForm):
    time = StringField("Time", validators=[DataRequired()])
    place = StringField("Place", validators=[DataRequired()])
    submit = SubmitField("Request Pass")
