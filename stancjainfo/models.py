from datetime import datetime
from enum import Enum

from flask_login import UserMixin

from stancjainfo import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    accepted = db.Column(db.Boolean, nullable=False, default=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    role = db.Column(db.String(20), nullable=False, default='USER')
    last_logged = db.Column(db.DateTime)
    posts = db.relationship('Post', backref='author', lazy=True)
    payments = db.relationship('InternetPayment', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Months(Enum):
    JAN = 1
    FEB = 2
    MAR = 3
    APR = 4
    MAY = 5
    JUN = 6
    JUL = 7
    AUG = 8
    SEP = 9
    OCT = 10
    NOV = 11
    DEC = 12


class InternetEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Enum(Months), nullable=False)
    year = db.Column(db.String, nullable=False)
    payment_amount = db.Column(db.Float(precision='4,2'), nullable=False)
    date_of_payment = db.Column(db.Date, nullable=False)
    penalty = db.Column(db.Float(precision='4,2'), nullable=False)
    payments = db.relationship('InternetPayment', backref='internet_entry', lazy=True)


class InternetPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    remaining_amount = db.Column(db.Float(precision='4,2'), nullable=False)
    already_paid_amount = db.Column(db.Float(precision='4,2'), nullable=False)
    payment_accepted_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    internet_entry_id = db.Column(db.Integer, db.ForeignKey('internet_entry.id'), nullable=False)


class MediaEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Enum(Months), nullable=False)
    year = db.Column(db.String, nullable=False)
    payment_amount = db.Column(db.Float(precision='4,2'), nullable=False)
    cold_water_kitchen = db.Column(db.Float(precision='4,2'), nullable=False)
    warm_water_kitchen = db.Column(db.Float(precision='4,2'), nullable=False)
    cold_water_bathroom = db.Column(db.Float(precision='4,2'), nullable=False)
    warm_water_bathroom = db.Column(db.Float(precision='4,2'), nullable=False)
    current = db.Column(db.Float(precision='4,2'), nullable=False)
    gas = db.Column(db.Float(precision='4,2'), nullable=False)
    current_refund = db.Column(db.Float(precision='4,2'), nullable=False)
