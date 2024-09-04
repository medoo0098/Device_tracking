from config import Config, db
from flask import Flask
from views import init_routes
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor

def create_app():
    app = Flask(__name__)  # initilizing flask app
    app.config.from_object(Config)  # reading config from Config object created in config.py
    db.init_app(app)  # initialising database within the app , created in config.py
    ckeditor = CKEditor(app)
    Bootstrap5(app)
    with app.app_context():  # within the app context we are creating tables, (all) created in models.py 
        db.create_all()  # fucntion to create all tables (models from models,py)
    
    init_routes(app)  # the fucntion to route all routes in a function called init route, created in routes.py

    return app  # app in returned as an value 


app = create_app()  # from fonction create app, flask app is being created


if __name__ == "__main__":  # 
    app.run(host="0.0.0.0", port=5001)