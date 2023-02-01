from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, EmailField, SelectField
from wtforms.validators import NumberRange, InputRequired


class voegGebruikerToe(FlaskForm):
    mail = StringField('Gebruikersnaam')
    password = StringField('Maak een wachtwoord')
    submit = SubmitField('Voeg toe')


class reserverenWeek(FlaskForm):
    week = IntegerField('Weeknummer', validators=[InputRequired(), NumberRange(1, 52, 'weeknummer buiten bereik')])
    submit = SubmitField('check beschikbaarheid')


class BoekenForm(FlaskForm):
    huis = SelectField('Gekozen huis')
    week = IntegerField('Weeknummer')
    gast = EmailField('Account(email adres)')
    wachtwoord = StringField('(Kies een) wachtwoord')
    submit = SubmitField('Reserveer')
