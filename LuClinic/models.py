
from sqlalchemy import ForeignKey
from .__init__ import dbAlchemy

#Maybe we use reflection or automapping if we need more than this..

dbAlchemy.Model.metadata.reflect(dbAlchemy.engine)

class Provider(dbAlchemy.Model):

    __table__ = dbAlchemy.Model.metadata.tables['provider']

    #providerID = dbAlchemy.Column(dbAlchemy.Integer, primary_key=True)
    #providerName = dbAlchemy.Column(dbAlchemy.String(30), nullable=False)
    #providerLicense = dbAlchemy.Column(dbAlchemy.String(10), nullable=False)
    #providerSpecialty = dbAlchemy.Column(dbAlchemy.String(30), nullable=False)
    #providerNPI =dbAlchemy.Column(dbAlchemy.String(10), nullable=False)
    #providerEmail =dbAlchemy.Column(dbAlchemy.String(255), unique=True)

class Patient(dbAlchemy.Model):

    __table__ = dbAlchemy.Model.metadata.tables['patient']

    #patientID = dbAlchemy.Column(dbAlchemy.Integer, primary_key=True)
    #patientName = dbAlchemy.Column(dbAlchemy.String(30), nullable=False)
    #patientAddress = dbAlchemy.Column(dbAlchemy.String(50), nullable=False)
    #patientPhone = dbAlchemy.Column(dbAlchemy.String(10), nullable=False)
    #patientPCP = dbAlchemy.Column(dbAlchemy.Integer, ForeignKey(Provider.providerID))
    #patientEmail = dbAlchemy.Column(dbAlchemy.String(255), unique=True)

class Login(dbAlchemy.Model):

    __table__ = dbAlchemy.Model.metadata.tables['login']

class Visit(dbAlchemy.Model):

    __table__ = dbAlchemy.Model.metadata.tables['visit']

class Message(dbAlchemy.Model):

    __table__ = dbAlchemy.Model.metadata.tables['message']

class Lab_Test(dbAlchemy.Model):

    __table__ = dbAlchemy.Model.metadata.tables['lab_test']

class Lab_Order(dbAlchemy.Model):

    __table__ = dbAlchemy.Model.metadata.tables['lab_order']

class Diagnosis(dbAlchemy.Model):

    __table__ = dbAlchemy.Model.metadata.tables['diagnosis']

class Health_Issues(dbAlchemy.Model):

    __table__ = dbAlchemy.Model.metadata.tables['health_issues']

class Medication(dbAlchemy.Model):

    __table__ = dbAlchemy.Model.metadata.tables['medication']

class Prescription(dbAlchemy.Model):

    __table__ = dbAlchemy.Model.metadata.tables['prescription']

class Allergen(dbAlchemy.Model):

    __table__ = dbAlchemy.Model.metadata.tables['allergen']

class Allergy(dbAlchemy.Model):

    __table__ = dbAlchemy.Model.metadata.tables['allergy']

dbAlchemy.create_all()
