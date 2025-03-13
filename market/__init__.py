from flask_bcrypt import Bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
flask_app = Flask(__name__)
flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
flask_app.config['SECRET_KEY']='a67eb58a3af0ce942c701374'
database = SQLAlchemy(flask_app)
bcrypt = Bcrypt(flask_app)
login_manager = LoginManager(flask_app)
login_manager.login_view = 'login_page'
login_manager.login_message_category= 'info'
from market import routes