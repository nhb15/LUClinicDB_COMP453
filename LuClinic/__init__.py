from flask import Flask
import yaml
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


# Configure db
# import pry; pry()
db = yaml.load(open('db.yaml'))
CONN_STR = "mysql://{}:{}@{}/{}".format(db['mysql_user'], db['mysql_password'], db['mysql_host'], db['mysql_db'])
app.config['MYSQL_HOST'] = db['mysql_host']
#app.config['MYSQL_PORT'] = int(db['mysql_port'])
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['SQLALCHEMY_DATABASE_URI'] = CONN_STR

mysql = MySQL(app)
dbAlchemy = SQLAlchemy(app)
engine = create_engine(CONN_STR)
#sqlAlchemy = engine.connect()


#Session = sessionmaker(bind=engine)

#alchemySession = Session()
