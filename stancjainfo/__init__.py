from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# TODO env var
app.config['SECRET_KEY'] = '34da334d734b00009983b65f33e48af7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
db.create_all()
db.session.commit()

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'light'
login_manager.login_message = 'Zaloguj się aby zobaczyć zawartość strony'

from stancjainfo import routes