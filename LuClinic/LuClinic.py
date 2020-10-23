# Please run the following in your prompt:
# pip install Flask-Session
# pip install pry.py

from flask import Flask, render_template, url_for, flash, redirect, request, session
from .forms import RegistrationForm, LoginForm, MedicationForm, AddPatientForm, ModifyPatientForm
from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor
import yaml
# from flask.ext.session import Session
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, current_user, login_required

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# Configure db
# import pry; pry()
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
#app.config['MYSQL_PORT'] = int(db['mysql_port'])
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

    cur.execute("SELECT pt.patientName, pt.patientAddress, prov.providerName FROM patient AS pt, provider AS prov WHERE pt.patientPCP = prov.providerID")
    patientTable = cur.fetchall()

    return render_template('testdb.html', patient=patient, message=message, provider=provider, visit=visit, patientTable=patientTable)

# LOGGED OUT FLOW -------------------->

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # To add logic based on login type
        # cur = mysql.connection.cursor()
        # cur.execute("SELECT * FROM patient")
        # patient = cur.fetchall()
        if form.email.data == 'Trevor@luc.edu' and form.password.data == 'pass':
            session['login_type'] = 'provider'
            session['username'] = form.email.data
            flash('Logged in successfully!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# currently redirects to login
@app.route("/")
@app.route("/home")
def home():
    return redirect(url_for('login'))

# currently redirects to login
@app.route("/logout")
def logout():
    # We clear all sessions
    session.clear()
    return redirect(url_for('login'))    

# Details to be added
@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Add patient/provder to respictive table with an insert
        # Also add email password and login_type to login table with an insert
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

# LOGGED IN FLOW -------------------->

@app.route("/profile")
# @login_required # This is a decorator to only allow user to see the page if they are logged in
def profile():
    # import pry; pry()
    email = session['username']
    if email is None:
      flash(f'Please login first!', 'danger')
    if session['login_type'] == 'provider':
        # Find the tuple using the email id
        # import pry; pry()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM provider where providerEmail = '%s'" % str(email))
        # Using fetchone instead of fetchall since we know it will return one value
        prvDetails = cur.fetchall()


        # create session['patient_id'] = patients_id from above query
        return render_template('provider_profile.html', title='Profile', provider_details=prvDetails)
    else:
        # Find the tuple using the email id in provider
        # cur = mysql.connection.cursor()
        # cur.execute("SELECT * FROM provider where email_id = email")
        # visit = cur.fetchall()
        # create session['provider_id'] = patients_id from above query
        return render_template('provider_profile.html', title='Provider')


@app.route("/addMedication", methods=['GET', 'POST'])
# @login_required # This is a decorator to only allow uer to see the page iof they are logged in
def addMedication():
    form = MedicationForm()
    if form.validate_on_submit():
        flash(f'Medicine {form.med.data} added!', 'success')
        return redirect(url_for('home'))
    return render_template('addMedication.html', title='Add a Medication', form=form)

@app.route("/addPatient", methods=['GET', 'POST'])
# @login_required # This is a decorator to only allow uer to see the page iof they are logged in
def addPatient():
    cur = mysql.connection.cursor()
    cur.execute("SELECT providerID, providerName FROM provider")
    providerNames = cur.fetchall()

    form = AddPatientForm()

    form.patientPCP.choices = providerNames
    if form.validate_on_submit():
        flash(f'Patient {form.patientName.data} added!', 'success')
        return redirect(url_for('profile'))
    return render_template('addPatient.html', title='Add a Patient', form=form)

@app.route("/myPatients")
def myPatients():
    email = session['username']
    cur = mysql.connection.cursor()
    cur.execute("SELECT providerID FROM provider WHERE providerEmail = '%s'" % email)
    providerID = cur.fetchone()

    cur.execute("SELECT DISTINCT patientID, patientName, patientPhone FROM patient WHERE patientPCP = '%d'" % providerID)
    patientTable = cur.fetchall()

    return render_template('myPatients.html', patientTable=patientTable)

@app.route("/modifyPatient/<patientID>", methods=['GET', 'POST'])
def modifyPatient(patientID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT providerID, providerName FROM provider")
    providerNames = cur.fetchall()

    form = ModifyPatientForm()

    form.patientPCP.choices = providerNames
    if form.validate_on_submit():
        flash(f'Patient {form.patientName.data} modified!', 'success')
        return redirect(url_for('myPatients'))
    return render_template('myPatients.html', title='Modify a Patient', form=form)




#Ideas for pages linking to provider profile: List appts (all or filtered by login provider?), list all patients, list MY patients, add patient, add provider, update patient, cancel appt(could be patient), etc

if __name__ == '__main__':
    app.run(debug=True)
