from config import Config, db
from flask import Flask
from views import init_routes
from models import User, ModDem
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


# initiating the flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MD.db'
ckeditor = CKEditor(app)
Bootstrap5(app)


# creating database in instance folder in application man folder

db = SQLAlchemy(model_class=Base)
db.init_app(app)


# creating all databases if not existing
with app.app_context():
    db.create_all()
    print("db is created")

init_routes(app, db)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)

    print("app running")

