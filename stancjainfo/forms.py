from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, DecimalField, \
    DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from stancjainfo.models import User, InternetEntry


class RegistrationForm(FlaskForm):
    username = StringField('Użytkownik',
                           validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Imię',
                           validators=[DataRequired(), Length(min=2, max=30)])
    surname = StringField('Nazwisko',
                           validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Hasło',
                             validators=[DataRequired(), Length(min=2, max=20)])
    confirm_password = PasswordField('Potwierdź hasło',
                                     validators=[DataRequired(), EqualTo('password'), Length(min=2, max=20)])
    submit = SubmitField('Zarejestruj')

    def validate_username(self, username):
        user = User.query.filter_by(username=str(username.data).lower()).first()
        if user:
            raise ValidationError('That username is already taken')

    def validate_email(self, email):
        user = User.query.filter_by(email=str(email.data).lower()).first()
        if user:
            raise ValidationError('That email is already taken')


class LoginForm(FlaskForm):
    username = StringField('Użytkownik',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Hasło',
                             validators=[DataRequired(), Length(min=2, max=20)])
    remember = BooleanField('Pamiętaj mnie')
    submit = SubmitField('Zaloguj')


class PostForm(FlaskForm):
    title = StringField('Nagłówek', validators=[DataRequired()])
    content = TextAreaField('Tekst', validators=[DataRequired()])
    submit = SubmitField('Dodaj')


class InternetEntryForm(FlaskForm):
    month = SelectField('Miesiąc', validators=[DataRequired()], coerce=str, choices=[
        ('JAN', 'Styczeń'),
        ('FEB', 'Luty'),
        ('MAR', 'Marzec'),
        ('APR', 'Kwiecień'),
        ('MAY', 'Maj'),
        ('JUN', 'Czerwiec'),
        ('JUL', 'Lipiec'),
        ('AUG', 'Sierpień'),
        ('SEP', 'Wrzesień'),
        ('OCT', 'Październik'),
        ('NOV', 'Listopad'),
        ('DEC', 'Grudzień')])
    year = SelectField('Rok', validators=[DataRequired()], coerce=int, choices=[
        (2017, '2017'),
        (2018, '2018'),
        (2019, '2019'),
        (2020, '2020')])
    payment_amount = DecimalField('Należność', validators=[DataRequired()], places=2)
    date_of_payment = DateField('Data zapłaty', validators=[DataRequired()])
    penalty = DecimalField('Kara', validators=[DataRequired()], places=2)
    submit = SubmitField('Dodaj')

    def validate_month(self, month):
        entry = InternetEntry.query.filter_by(month=month.data, year=int(self.year.data)).first()
        if entry:
            raise ValidationError('Entry for that month already exists')
