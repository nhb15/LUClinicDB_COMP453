import yaml
db = yaml.load(open('db.yaml'))

class Patient(db.Model):
    patientID = db.Column(db.Integer, primary_key=True)
    patientName = db.Column(db.String(30), nullable=False)
    patientAddress = db.Column(db.String(50), nullable=False)
    patientPhone = db.Column(db.String(10), nullable=False)
    patientEmail = db.Column(db.String(255), unique=True)

