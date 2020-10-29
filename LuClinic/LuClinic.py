# Please run the following in your prompt:
# pip install Flask-Session
# pip install pry.py

from flask import Flask, render_template, url_for, flash, redirect, request, session
from .forms import RegistrationForm, LoginForm, MedicationForm, AddPatientForm, ModifyPatientForm
from sqlalchemy.orm import sessionmaker, Session

from MySQLdb.cursors import DictCursor

# from flask.ext.session import Session
from flask_sqlalchemy import SQLAlchemy

from .models import Patient, Provider
from .__init__ import mysql, dbAlchemy, app, alchemySession
# from flask_login import LoginManager, current_user, login_required


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

    testQuery = alchemySession.query(Patient.patientName)

    return render_template('testdb.html', patient=patient, message=message, provider=provider, visit=visit, patientTable=patientTable, testQuery=testQuery)

# LOGGED OUT FLOW -------------------->

@app.route("/login", methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    # Reasons for login table: We run search on email and password on a smaller table.
    # We only query customer/provider tables once we need to load the profile pages.
    # We dont ask the user to mention whether they are patient or provider

    cur = mysql.connection.cursor()
    cur.execute("SELECT loginType FROM login where email = %s AND password = %s", (form.email.data, form.password.data))

    loginType = cur.fetchone()

    if loginType:
      session['email'] = form.email.data
      session['loginType'] = 'pat' if loginType[0] == 'pat' else 'prv'
      #import pry; pry()
      flash('Logged in successfully!', 'success')
      return redirect(url_for('profile'))
    else:
      flash('Login Unsuccessful. Please check username and password', 'danger')
      render_template('login.html', title='Login', form=form)

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
  if session['email']:
    email = session['email']
    if session['loginType'] == 'prv':
        # Find the tuple using the email id
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM provider where providerEmail = '%s'" % str(email))
        # Using fetchone instead of fetchall since we know it will return one value
        prvDetails = cur.fetchall()
        # session['providerId'] = patients_id from above query
        return render_template('provider_profile.html', title='Profile', provider_details=prvDetails)
    else:
        # Find the tuple using the email id in provider
        # cur = mysql.connection.cursor()
        # cur.execute("SELECT * FROM provider where email_id = email")
        # visit = cur.fetchall()
        # create session['provider_id'] = patients_id from above query
        return render_template('patient_profile.html', title='Patient')
  else:
    flash(f'Please login first!', 'danger')
    return redirect(url_for('login'))


@app.route("/addMedication", methods=['GET', 'POST'])
# @login_required # This is a decorator to only allow user to see the page if they are logged in
def addMedication():
    form = MedicationForm()
    if form.validate_on_submit():
        flash(f'Medicine {form.med.data} added!', 'success')
        return redirect(url_for('home'))
    return render_template('addMedication.html', title='Add a Medication', form=form)

@app.route("/addPatient", methods=['GET', 'POST'])
# @login_required # This is a decorator to only allow user to see the page if they are logged in
def addPatient():
    cur = mysql.connection.cursor()
    cur.execute("SELECT providerID, providerName FROM provider")
    providerNames = cur.fetchall()

    form = AddPatientForm()

    form.patientPCP.choices = providerNames
    if form.validate_on_submit():
        #FIXME: perform addition AND any necesary specific validations
        flash(f'Patient {form.patientName.data} added!', 'success')
        return redirect(url_for('profile'))
    return render_template('addPatient.html', title='Add a Patient', form=form)

@app.route("/myPatients")
# @login_required # This is a decorator to only allow uer to see the page if they are logged in
def myPatients():
    email = session['email']
    cur = mysql.connection.cursor()
    cur.execute("SELECT providerID FROM provider WHERE providerEmail = '%s'" % email)
    providerID = cur.fetchone()

    cur.execute("SELECT DISTINCT patientID, patientName, patientPhone FROM patient WHERE patientPCP = '%d'" % providerID)
    patientTable = cur.fetchall()

    cur.execute("SELECT DISTINCT COUNT(patientID) FROM patient WHERE patientPCP = '%d'" % providerID)
    patientCount = cur.fetchone()

    return render_template('myPatients.html', patientTable=patientTable, patientCount=patientCount)

@app.route("/modifyPatient/<patientID>", methods=['GET', 'POST'])
# @login_required # This is a decorator to only allow uer to see the page if they are logged in
def modifyPatient(patientID):

    form = ModifyPatientForm()
    #patient = Patient.query.get_or_404(patientID)
    patient = alchemySession.query(Patient).filter(Patient.patientID == patientID).first()

    #Populate SelectField with potential provider names
    cur = mysql.connection.cursor()
    cur.execute("SELECT providerID, providerName FROM provider")
    providerNames = cur.fetchall()
    form.patientPCP.choices = providerNames

    if form.validate_on_submit():
        #FIXME: perform modification
        #setattr(patient, 'patientName', form.patientName.data)
        #alchemySession.add(patient)
        #patient.patientName = form.patientName.data
        #patient.patientAddress = form.patientAddress.data
        #patient.patientPhone = form.patientPhone.data
        #patient.patientEmail = form.patientEmail.data
        #patient.patientPCP = form.patientPCP.data

        #Patient.query(Patient).filter_by(patientID == patientID).update({'patientName' : form.patientName.data})
        dbAlchemy.session.query(Patient).filter_by(patientID = patientID).update(dict(patientName=form.patientName.data, patientAddress=form.patientAddress.data, patientPhone=form.patientPhone.data, patientEmail=form.patientEmail.data, patientPCP=form.patientPCP.data))

        dbAlchemy.session.commit()
        flash(f'Patient {form.patientName.data} modified!', 'success')
        return redirect(url_for('myPatients'))

    elif request.method == 'GET':
        form.patientName.data = patient.patientName
        form.patientAddress.data = patient.patientAddress
        form.patientPhone.data = patient.patientPhone
        form.patientEmail.data = patient.patientEmail
        form.patientPCP.data = patient.patientPCP
    return render_template('modifyPatient.html', title='Modify a Patient', form=form)

@app.route("/deletePatient/<patientID>", methods=['POST'])
# @login_required # This is a decorator to only allow uer to see the page if they are logged in
def delete_patient(patientID):
    patient = Patient.query.get_or_404(patientID)
    dbAlchemy.session.delete(patient)
    dbAlchemy.session.commit()
    flash('The patient has been deleted!', 'success')
    return redirect(url_for('myPatients'))

#Ideas for pages linking to provider profile: List appts (all or filtered by login provider?), list all patients, list MY patients, add patient, add provider, update patient, cancel appt(could be patient), etc

if __name__ == '__main__':
    app.run(debug=True)
