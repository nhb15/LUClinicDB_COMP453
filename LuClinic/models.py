
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



dbAlchemy.create_all()