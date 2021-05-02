from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from forms import *
from datetime import date as dt
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Student(db.Model):
    name = db.Column(db.String(250), nullable=False)
    roll_number = db.Column(db.String(250), primary_key=True)
    phone_number = db.Column(db.Integer, nullable=False)
    parents_number = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(250), nullable=False)
    year_section = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)


class Warden(db.Model):
    name = db.Column(db.String(250), nullable=False)
    roll_number = db.Column(db.String(250), primary_key=True)
    phone_number = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(250), nullable=False)


class Passes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    roll_number = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(250), nullable=False)
    parents_number = db.Column(db.String(250), nullable=False)
    time = db.Column(db.String(250), nullable=False)
    place = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    reason = db.Column(db.String(250), nullable=False)
    status = db.Column(db.String(250), nullable=False)


db.create_all()
db.session.commit()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create/warden/<string:mess>", methods=["POST", "GET"])
def create_new_warden(mess):
    form = NewWarden()
    if form.validate_on_submit():
        data = Warden.query.filter_by(roll_number=form.roll_number.data).first()

        if data == None:
            db.session.add(Warden(
                name=form.name.data,
                roll_number=form.roll_number.data,
                phone_number=form.phone_number.data,
                password=generate_password_hash(password=form.password.data, method="pbkdf2:sha256", salt_length=8)
            ))
            db.session.commit()
            return redirect(url_for('create_new_warden', mess="New Warden Added Successfully"))

        else:
            mess = "User Exists"
    return render_template('admin_home.html', form=form, message=mess)


@app.route("/login", methods=["POST", "GET"])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == "adminHere" and form.password.data == "admin_secret":
            return redirect(url_for('create_new_warden', mess=" "))

        else:
            if form.login_type.data == "Warden":
                data = Warden.query.filter_by(roll_number=form.username.data).first()
                if data is None:
                    error = "User doesn't Exist"

                else:
                    if check_password_hash(data.password, form.password.data):
                        return redirect(url_for('warden_screen_pending'))

                    else:
                        error = "Incorrect Password"

            elif form.login_type.data == "Student":
                data = Student.query.filter_by(roll_number=form.username.data).first()
                if data is None:
                    error = "User doesn't Exist"

                else:
                    if check_password_hash(data.password, form.password.data):
                        return redirect(url_for('student_home', id=form.username.data))

                    else:
                        error = "Incorrect Password"

            else:
                error = "Select a login Type (Warden / Student)"

    return render_template('login.html', form=form, error=error)


# all warden paths
@app.route("/warden")
def warden_screen_pending():
    all_posts = Passes.query.filter_by(status="waiting").all()
    return render_template('wardenLogin.html', all_posts=all_posts)


@app.route("/accept_pass/<string:id>")
def accept_pass(id):
    data = Passes.query.filter_by(id=id).first()
    data.status = "accepted"
    db.session.commit()
    all_posts = Passes.query.filter_by(status="waiting").all()
    return render_template('wardenLogin.html', all_posts=all_posts)


@app.route("/reject_pass/<string:id>")
def reject_pass(id):
    data = Passes.query.filter_by(id=id).first()
    data.status = "rejected"
    db.session.commit()
    all_posts = Passes.query.filter_by(status="waiting").all()
    return render_template('wardenLogin.html', all_posts=all_posts)


@app.route("/warden/completedb")
def completeDB():
    all_posts = db.session.query(Passes).all()
    return render_template('completedb.html', all_posts=all_posts)


@app.route("/warden/completeStudentdb")
def completeStudentDB():
    all_posts = db.session.query(Student).all()
    return render_template('completeStudentDB.html', all_posts=all_posts)


@app.route("/create/student/<string:mess>", methods=["POST", "GET"])
def create_new_student(mess):
    form = NewStudent()
    if form.validate_on_submit():
        data = Student.query.filter_by(roll_number=form.roll_number.data).first()

        if data == None:
            db.session.add(Student(
                name=form.name.data,
                roll_number=form.roll_number.data,
                phone_number=form.phone_number.data,
                department=form.department.data,
                year_section=form.year_section.data,
                parents_number=form.parents_number.data,
                password=generate_password_hash(password=form.password.data, method="pbkdf2:sha256", salt_length=8)
            ))
            db.session.commit()
            return redirect(url_for('create_new_student', mess="New Student Added Successfully"))

        else:
            mess = "User Exists"
    return render_template('addnewStudent.html', form=form, message=mess)


# all student paths
@app.route("/create/pass/<string:id>", methods=["POST", "GET"])
def create_new_pass(id):
    form = RegisterGatepass()
    if form.validate_on_submit():
        data = Student.query.filter_by(roll_number=id).first()
        if data is None:
            pass
        else:
            db.session.add(Passes(
                name=data.name,
                reason=form.reason.data,
                roll_number=data.roll_number,
                phone_number=data.phone_number,
                parents_number=data.parents_number,
                time=form.time.data,
                place=form.place.data,
                date=f"{dt.today()}",
                status="waiting"
            ))
            db.session.commit()
            return redirect(url_for('student_home', id=id))
    return render_template('createGatepass.html', form=form)


@app.route("/student/<string:id>")
def student_home(id):
    all_posts = Passes.query.filter_by(roll_number=id).all()
    return render_template('studentHome.html', all_posts=all_posts, id=id)


@app.route("/student/reset_password", methods=["POST", "GET"])
def student_reset_password():
    form = ResetPasswordStudent()
    error = None
    if form.validate_on_submit():
        data = Student.query.filter_by(roll_number=form.roll_number.data).first()

        if data == None:
            error = "No user with that Roll Number in the Database"
        else:
            if check_password_hash(data.password, form.old_password.data):
                password = generate_password_hash(password=form.password.data, method="pbkdf2:sha256", salt_length=8)
                data.password = password
                db.session.commit()
            else:
                error = "Old Password incorrect"
    return render_template('student_reset_password.html', form=form, error=error)


if __name__ == "__main__":
    app.run(debug=True)
