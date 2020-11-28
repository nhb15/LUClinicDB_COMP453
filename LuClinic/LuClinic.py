from flask import Flask, render_template, url_for, flash, redirect, request, session
from .forms import RegistrationForm, LoginForm, MedicationForm, AddPatientForm, ModifyPatientForm, replyMessageForm, ActivatePatientForm, RegisterProviderForm
from datetime import datetime
from sqlalchemy.orm import sessionmaker, Session

from MySQLdb.cursors import DictCursor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import intersect, func
from .models import Patient, Provider, Visit, Message, Prescription, Login, Diagnosis, Medication, Allergen, Allergy, Lab_Order, Lab_Test, Health_Issues
from .__init__ import mysql, dbAlchemy, app
import ipdb

@app.route("/testdb")
def testdb():
    # import pry; pry()
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

    testQuery = dbAlchemy.session.query(Patient.patientName)

    return render_template('testdb.html', patient=patient, message=message, provider=provider, visit=visit, patientTable=patientTable, testQuery=testQuery)


# LOGGED OUT FLOW -------------------->


# currently redirects to login
@app.route("/")
@app.route("/home")
def home():
  return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    if form.email.data == 'admin@luc.edu' and form.password.data == 'admin':
      session['email'] = 'admin@luc.edu'
      return redirect(url_for('admin'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT loginType FROM login where email = %s AND password = %s", (form.email.data, form.password.data))

    loginType = cur.fetchone()

    if loginType:
      session['email'] = form.email.data
      session['loginType'] = 'pat' if loginType[0] == 'pat' else 'prv'
      flash('Logged in successfully!', 'success')
      return redirect(url_for('profile'))
    else:
      flash('Login Unsuccessful. Please check username and password', 'danger')
      render_template('login.html', title='Login', form=form)

  return render_template('login.html', title='Login', form=form)

# currently redirects to login
@app.route("/logout")
def logout():
  session.clear()
  return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
  return render_template('register.html')

@app.route("/activatePatient", methods=['GET', 'POST'])
def activatePatient():
  form = ActivatePatientForm()
  if form.validate_on_submit():

      cur = mysql.connection.cursor()
      cur.execute("SELECT patientEmail FROM patient where patientEmail = '%s'" % form.email.data)

      patientDetails = cur.fetchone()

      if patientDetails:
        cur.execute("SELECT email FROM login where email = '%s'" % form.email.data)
        login_exists = cur.fetchone()

        if login_exists:
          flash('Patient Already exists, please login', 'danger')
          return redirect(url_for('login'))
        else:

            login = Login(email=form.email.data, password=form.password.data, loginType='pat')
            dbAlchemy.session.add(login)
            dbAlchemy.session.commit()
            #cur.execute("INSERT INTO login VALUES (%s, %s, 'pat')", (form.email.data, form.password.data))

            flash(f'Account registered for {patientDetails[0]}! Please login with your new credentials', 'success')
      else:
        flash('Registration Failed. Please check email or contact your doctor.', 'danger')
      return redirect(url_for('register'))
  return render_template('activate_patient.html', title='ActivatePatient', form=form)

@app.route("/registerProvider", methods=['GET', 'POST'])
def registerProvider():
  form = RegisterProviderForm()
  if form.validate_on_submit():
    cur = mysql.connection.cursor()
    cur.execute("SELECT email FROM login where email = '%s'" % form.providerEmail.data)
    login_exists = cur.fetchone()

    if login_exists:
      flash('Provider Already exists, please login', 'danger')
      return redirect(url_for('login'))
    else:

      provider = Provider(providerLicense=form.providerLicense.data, providerSpecialty=form.providerSpeciality.data, providerNPI=form.providerNPI.data, providerEmail=form.providerEmail.data, providerName=form.providerName.data)
      login = Login(email=form.providerEmail.data, password=form.password.data, loginType='prv')
      dbAlchemy.session.add(provider)
      dbAlchemy.session.commit()
      dbAlchemy.session.add(login)
      dbAlchemy.session.commit()

      flash(f'Provider Account created! Please login with your new credentials', 'success')
      return redirect(url_for('login'))
  return render_template('register_provider.html', title='RegisterProvider', form=form)


# LOGGED IN FLOW -------------------->


@app.route("/profile")
def profile():
  if session['email']:
    email = session['email']
    if session['loginType'] == 'prv':
      cur = mysql.connection.cursor()
      cur.execute("SELECT * FROM provider where providerEmail = '%s'" % str(email))
      prvDetails = cur.fetchall()
      return render_template('provider_profile.html', title='Provider Profile', provider_details=prvDetails)
    else:

        # Find the tuple using the email id in patient
        cur = mysql.connection.cursor()

        cur.execute("SELECT patientID FROM patient WHERE patientEmail = '%s'" % email)
        patientID = cur.fetchone()

        cur.execute("SELECT patientName, patientAddress, patientPhone, patientEmail, providerName FROM patient, provider WHERE patient.patientPCP = provider.providerID AND patient.patientEmail = '%s'" % str(email))
        patient_details = cur.fetchall()

        visits = Visit.query.join(Patient, Visit.patientID == Patient.patientID). \
        join(Provider, Patient.patientPCP == Provider.providerID). \
        filter(Visit.patientID == patientID, Visit.visitStatus == 'Scheduled'). \
        add_columns(Visit.visitDate, Visit.visitStatus, Visit.providerID, Provider.providerName)

        #cur.execute("SELECT providerID, visitDate, visitStatus FROM patient, visit WHERE visit.patientID = '%d' AND visit.patientID = patient.patientID AND visitStatus = 'Scheduled'" % patientID)
        #visits = cur.fetchall()

        labOrders = Lab_Order.query.join(Lab_Test, Lab_Test.cpt == Lab_Order.cpt). \
        filter(Lab_Order.completeDate == None, Lab_Order.patientID == patientID). \
        add_columns(Lab_Test.labName)

        #cur.execute("SELECT labName FROM patient, lab_test, lab_order WHERE patient.patientID = lab_order.patientID AND lab_test.cpt = lab_order.cpt AND completeDate IS NULL AND lab_order.patientID = '%d'" %patientID)
        #labOrders = cur.fetchall()

        meds = Prescription.query.join(Medication, Prescription.medID == Medication.medID). \
        filter(Prescription.patientID == patientID). \
        add_columns(Medication.medName, Prescription.dosage)

        allergies = Allergy.query.join(Allergen, Allergy.allergenID == Allergen.allergenID). \
        filter(Allergy.patientID == patientID). \
        add_columns(Allergen.allergenName)

        issues = Health_Issues.query.join(Diagnosis, Health_Issues.icd_10_cm == Diagnosis.icd_10_cm). \
        filter(Health_Issues.patientID == patientID). \
        add_columns(Diagnosis.diagnosisName)

        # create session['provider_id'] = patients_id from above query
        return render_template('patient_profile.html', title='Patient Profile', patient_details=patient_details, visits=visits, labOrders=labOrders, meds=meds, allergies=allergies, issues=issues)

  else:
    flash(f'Please login first!', 'danger')
    return redirect(url_for('login'))


@app.route("/myPatients")
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


@app.route("/addPatient", methods=['GET', 'POST'])
# Send email to LOGIN for this and modifyPatient and check email validator
def addPatient():
    cur = mysql.connection.cursor()
    cur.execute("SELECT providerID, providerName FROM provider")
    providerNames = cur.fetchall()

    form = AddPatientForm()

    form.patientPCP.choices = providerNames
    if form.validate_on_submit():

        patient = Patient(patientName=form.patientName.data, patientAddress=form.patientAddress.data, patientPhone=form.patientPhone.data, patientEmail=form.patientEmail.data, patientPCP=form.patientPCP.data)
        dbAlchemy.session.add(patient)
        dbAlchemy.session.commit()

        flash(f'Patient {form.patientName.data} added!', 'success')
        return redirect(url_for('profile'))
    return render_template('addPatient.html', title='Add a Patient', form=form)


@app.route("/modifyPatient/<patientID>", methods=['GET', 'POST'])
# @login_required # This is a decorator to only allow user to see the page if they are logged in
# Send email to LOGIN for this and modifyPatient and check email validator
def modifyPatient(patientID):

    form = ModifyPatientForm()
    #patient = Patient.query.get_or_404(patientID)
    patient = dbAlchemy.session.query(Patient).filter(Patient.patientID == patientID).first()

    #Populate SelectField with potential provider names
    cur = mysql.connection.cursor()
    cur.execute("SELECT providerID, providerName FROM provider")
    providerNames = cur.fetchall()
    form.patientPCP.choices = providerNames
    form.patientID = patientID

    if form.validate_on_submit():

            dbAlchemy.session.query(Patient).filter_by(patientID = patientID).update(dict(patientName=form.patientName.data, patientAddress=form.patientAddress.data, patientPhone=form.patientPhone.data, patientPCP=form.patientPCP.data))

            dbAlchemy.session.commit()
            flash(f'Patient {form.patientName.data} modified!', 'success')
            return redirect(url_for('myPatients'))
        #else:
         #   form.patientEmail.errors.append('test error')

    elif request.method == 'GET':
        form.patientName.data = patient.patientName
        form.patientAddress.data = patient.patientAddress
        form.patientPhone.data = patient.patientPhone
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

@app.route("/addMedication", methods=['GET', 'POST'])
# @login_required # This is a decorator to only allow user to see the page if they are logged in
def addMedication():
    form = MedicationForm()
    if form.validate_on_submit():
        flash(f'Medicine {form.med.data} added!', 'success')
        return redirect(url_for('home'))
    return render_template('addMedication.html', title='Add a Medication', form=form)


#is there anything differentiating how patients vs. providers access this or is it just based on what renders on their profile page?
@app.route("/appointments", methods=['GET'])
def appointments():
    email = session['email']

    patient_info = Patient.query.filter_by(patientEmail=email).first()

    appointments = Visit.query.join(Provider, Visit.providerID == Provider.providerID). \
    filter(Visit.patientID == patient_info.patientID). \
    add_columns(Provider.providerName, Visit.visitDate, Visit.visitStatus, Visit.visitID)

    return render_template('appointments.html', appointments=appointments)


@app.route("/visit/<visitID>", methods=['GET'])
def visit(visitID):
    visit = Visit.query.join(Provider, Visit.providerID == Provider.providerID). \
    filter(Visit.visitID == visitID). \
    add_columns(Visit.visitDate, Visit.visitID, Provider.providerName).first()
    return render_template('visit.html', title=visit.visitID, visit=visit)


@app.route("/visit/<visitID>/cancel", methods=['POST'])
def cancel_visit(visitID):
    visit = Visit.query.get_or_404(visitID)
    dbAlchemy.session.delete(visit)
    dbAlchemy.session.commit()
    flash('Your appointment has been cancelled.', 'success')
    return redirect(url_for('appointments'))

#Ideas for pages linking to provider profile: list all patients, list MY patients, add patient, add provider, update patient, etc


@app.route("/messages", methods=['GET', 'POST'])
# @login_required # This is a decorator to only allow uer to see the page if they are logged in
def myMessages():

    email = session['email']
    cur = mysql.connection.cursor()

    if session['loginType'] == 'prv':

        cur.execute("SELECT providerID FROM provider WHERE providerEmail = '%s'" % email)
        providerID = cur.fetchone()

        #Need to figure out best way to order by
        cur.execute("SELECT mess.messageID, mess.messageSubject, mess.messageBody, mess.messageDate, pat.patientName, mess.senderPT FROM message AS mess INNER JOIN patient AS pat USING (patientID) WHERE mess.providerID = '%d' ORDER BY mess.messageDate DESC " % providerID)
        messages = cur.fetchall()

        return render_template('provider_message.html', providerID=providerID, messages=messages)
    else:
        cur.execute("SELECT patientID FROM patient WHERE patientEmail = '%s'" % email)
        patientID = cur.fetchone()

        #Need to figure out best way to order by
        cur.execute("SELECT mess.messageID, mess.messageSubject, mess.messageBody, mess.messageDate, prov.providerName, mess.senderPT FROM message AS mess INNER JOIN provider AS prov USING (providerID) WHERE mess.patientID = '%d' ORDER BY mess.messageDate DESC " % patientID)
        messages = cur.fetchall()
        return render_template('patient_message.html', patientID=patientID, messages=messages)


@app.route("/messages/<messageID>/reply", methods=['GET', 'POST'])
# @login_required # This is a decorator to only allow uer to see the page if they are logged in
def replyMessage(messageID):

    form = replyMessageForm()
    #Should be include message history? Maybe by searching over same patient-provider with same subject?
    message = Message.query.get_or_404(messageID)

    cur = mysql.connection.cursor()
    cur.execute("SELECT mess.messageID, mess.messageSubject, mess.messageBody, mess.messageDate, pat.patientName, mess.senderPT, prov.providerName FROM message AS mess INNER JOIN patient AS pat USING (patientID) INNER JOIN provider AS prov USING (providerID) WHERE mess.messageSubject = '%s' AND mess.patientID = '%d' AND mess.providerID = '%d' ORDER BY mess.messageDate DESC" % (message.messageSubject, message.patientID, message.providerID))
    messageHistory = cur.fetchall()

    if session['loginType'] == 'prv':
        template = 'provider_reply_message.html'
        senderPT = 0
    else:
        template = 'patient_reply_message.html'
        senderPT = 1

    if form.validate_on_submit():

        newMessage = Message(messageSubject=form.messageSubject.data, messageBody=form.messageBody.data, patientID=message.patientID, providerID=message.providerID, messageDate=datetime.now(), senderPT=senderPT)
        dbAlchemy.session.add(newMessage)
        dbAlchemy.session.commit()
        flash(f'Message sent!', 'success')
        return redirect(url_for('myMessages'))

    elif request.method == 'GET':
        form.messageSubject.data = message.messageSubject

    return render_template(template, message=message, messageHistory=messageHistory, form=form)

@app.route("/admin", methods=['GET'])
def admin():
    if session['email'] != 'admin@luc.edu':
      return redirect(url_for('login'))
    
    # Total upcoming appointments in next Month
    totalUpcomingAppointments = dbAlchemy.session.query(Visit).filter(Visit.visitStatus=='Scheduled').count() # 5

    # Total Completed Appointments
    totalCompletedAppointments = dbAlchemy.session.query(Visit).filter(Visit.visitStatus=='Completed').count() # 6

    # INTERSECT COMPOUND
    # Patients that have visited and messaged
    # Distinct patients from visit and messages
    # SQL
    # Out of 6 patients on 1,3,4 and 6 have both visited and messaged
    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT patientID FROM message INTERSECT SELECT DISTINCT patientID FROM visit") # 1,3,4 and 6
    patientCommunication = cur.fetchall()
    
    # Patients that have both Atorvastatin and Omeprazole prescribed
    # Shows compond sql in Alchemy
    ator = dbAlchemy.session.query(Prescription.patientID).filter(Prescription.medID==4)
    omep = dbAlchemy.session.query(Prescription.patientID).filter(Prescription.medID==7)
    medCombinations = ator.intersect(omep).all()
    #medCombinations = intersect(Prescription.select(Prescription.patientID).where(Prescription.medID==4).distinct(), Prescription.select(Prescription.patientID).where(Prescription.medID==7).distinct())
   
    # Group BY SQLALchemy
    # Providers with most vists and count.
    providerVisitCount = dbAlchemy.session.query(Visit.providerID, func.count(Visit.providerID)).group_by(Visit.providerID).all()
    
    # Subquery and somewhat a complex query
    # List of all Patients that have been prescribed 'mg' dosage
    subquery = dbAlchemy.session.query(Prescription.patientID).filter(Prescription.dosage.like('%mg%')).subquery()
    mgDose = dbAlchemy.session.query(Patient).filter(Patient.patientID.in_(subquery)).all()
   
    return render_template('admin.html', mgDose=mgDose, totalUpcomingAppointments=totalUpcomingAppointments, totalCompletedAppointments=totalCompletedAppointments, patientCommunication=patientCommunication, medCombinations=medCombinations, providerVisitCount=providerVisitCount)

# Details to be added
@app.route("/about")
def about():
  return render_template('about.html', title='About')

if __name__ == '__main__':
    app.run(debug=True) 
