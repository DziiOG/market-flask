#init file
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# __name__ referring to local python file
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY']= 'fd771671168d3b72b7f290b3'

#initialise db
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

#redurect to login to page if not logged in
login_manager.login_view = "login_page"
login_manager.login_message_category = 'info'

from src.routes import endpoints






