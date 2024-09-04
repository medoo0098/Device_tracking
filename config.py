import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import logging


# import enviromental variables 
load_dotenv()  # makking .env file easilly accessible for the fucntion to call os.getenv( " database url")




class Config:  
    """
    configuring the app parameters 
    
    """
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")  # gets the database url from specified location in here its from .env as a enviroment variable
    SQLAlchemy_TRACK_MODIFICATIONS = True  # when changes are done in DB , chnages will apear in the terminal
    DEBUG = True
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    SECRET_KEY = os.getenv("SECRET_KEY")

db = SQLAlchemy()



