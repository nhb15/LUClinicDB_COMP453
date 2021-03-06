from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, ValidationError, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, StopValidation
from wtforms.widgets import HiddenInput

from .__init__ import dbAlchemy
from .models import Patient, Login, Provider

class RegisterProviderForm(FlaskForm):
    providerLicense = StringField('License Number', validators=[DataRequired(),Length(min=1, max=10)])
    providerSpeciality = StringField('Speciality', validators=[DataRequired()])
    providerNPI = StringField('NPI', validators=[DataRequired(),Length(min=1, max=10)])
    providerName = StringField('Name', validators=[DataRequired()])
    providerEmail = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class ActivatePatientForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # remember = BooleanField('Remember Me')
    # patientType = BooleanField('Patient')
    # providerType = BooleanField('Provider')
    submit = SubmitField('Login')

class MedicationForm(FlaskForm):
    med = StringField('Medication', validators=[DataRequired()])
    dailyFreq = IntegerField('Number of Times Taken Daily', validators=[DataRequired(), NumberRange(min=0, max=None)])
    submit = SubmitField('Add this medication')

class ModifyPatientForm(FlaskForm):
    #FIXME: Updating an email should technically update the login table

    patientID = HiddenField()
    patientName = StringField("Patient Name", validators=[DataRequired(),Length(min=1, max=30)])
    patientAddress = StringField("Patient Address", validators=[DataRequired(),Length(min=1, max=50)])
    patientPhone = StringField("Patient Phone", validators=[DataRequired(),Length(min=1, max=10)])
    patientPCP = SelectField("Patient PCP", coerce=int, validators=[DataRequired()])
    submit = SubmitField('Confirm changes on this patient')

    #Validation unneeded- we will not allow providers to change patient emails. If we wanted this, we could validate it against the login table as needed (as long as patientID or providerID are checked as well)
    #def validatePatientEmail(self):
    #    patient = dbAlchemy.session.query(Patient).filter_by(patientEmail=self.patientEmail.data).first()

    #    provider = dbAlchemy.session.query(Provider).filter_by(providerEmail=self.patientEmail.data).first()
    #    if (patient and patient.patientID != self.patientID) or provider:
    #        return 0
            #raise ValidationError('That email is already being used. Please enter a different one!')

class AddPatientForm(ModifyPatientForm):
    #Inherit from Modify Patient Form - change the submit button.
    #patientName = StringField("Patient Name", validators=[DataRequired(),Length(min=1, max=30)])
    #patientAddress = StringField("Patient Address", validators=[DataRequired(),Length(min=1, max=50)])
    #patientPhone = StringField("Patient Phone", validators=[DataRequired(),Length(min=1, max=10)])
    patientEmail = StringField("Patient Email", validators=[DataRequired(), Email()])
    #patientPCP = SelectField("Patient PCP", coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add this patient')

class replyMessageForm(FlaskForm):

    messageID = HiddenField()
    patientID = HiddenField()
    providerID = HiddenField()
    messageSubject = StringField("Subject", validators=[DataRequired(), Length(min=1, max=30)])
    messageBody = TextAreaField("Body", validators=[DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Send Message')

#Ideas for forms: Update Patient, Delete (cancel) appointment, Create Appt
