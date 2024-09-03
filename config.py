from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor



# initiating the flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MD.db'
ckeditor = CKEditor(app)
Bootstrap5(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass



# creating database in instance folder in application man folder

db = SQLAlchemy(model_class=Base)
db.init_app(app)