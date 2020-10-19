from flask import Flask, render_template, url_for, flash, redirect, request
from .forms import RegistrationForm, LoginForm, MedicationForm
from flask_mysqldb import MySQL
import yaml
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_required

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_PORT'] = int(db['mysql_port'])
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route("/testdb")
def testdb():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patient")
    patient = cur.fetchall()
    cur.execute("SELECT * FROM message")
    message = cur.fetchall()
    cur.execute("SELECT * FROM provider")
    provider = cur.fetchall()
    cur.execute("SELECT * FROM visit")
    visit = cur.fetchall()

    return render_template('testdb.html', patient=patient, message=message, provider=provider, visit=visit)

# LOGGED OUT FLOW -------------------->

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # To add logic based on login type
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('Welcome to', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# currently redirects to login
@app.route("/")
@app.route("/home")
def home():
    return redirect(url_for('login'))

# Details to be added
@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

# LOGGED IN FLOW -------------------->

@app.route("/profile")
@login_required # This is a decorator to only allow uer to see the page iof they are logged in
def profile():
    if form.login_type.data == 'patient':
      cur = mysql.connection.cursor()
      cur.execute("SELECT * FROM patient")
      pname = cur.fetchall()
      return render_template('patient_profile.html', title='Profile', patient_name=pname)
    else:
      return render_template('provider_profile.html', title='Provider')


@app.route("/addMedication", methods=['GET', 'POST'])
@login_required # This is a decorator to only allow uer to see the page iof they are logged in
def addMedication():
    form = MedicationForm()
    if form.validate_on_submit():
        flash(f'Medicine {form.med.data} added!', 'success')
        return redirect(url_for('home'))
    return render_template('addMedication.html', title='Add a Medication', form=form)

if __name__ == '__main__':
    app.run(debug=True)
