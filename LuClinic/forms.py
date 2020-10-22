from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class MedicationForm(FlaskForm):
    med = StringField('Medication', validators=[DataRequired()])
    dailyFreq = IntegerField('Number of Times Taken Daily', validators=[DataRequired(), NumberRange(min=0, max=None)])
    submit = SubmitField('Add this medication')

class AddPatientForm(FlaskForm):
    patientName = StringField("Patient Name", validators=[DataRequired(),Length(min=1, max=30)])
    patientAddress = StringField("Patient Address", validators=[DataRequired(),Length(min=1, max=50)])
    patientPhone = StringField("Patient Phone", validators=[DataRequired(),Length(min=1, max=10)])
    patientEmail = StringField("Patient Email", validators=[DataRequired(), Email()])
    patientPCP = SelectField("Patient PCP", coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add this patient')
    