from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, EmailField, FloatField, SelectField
from wtforms.validators import NumberRange, InputRequired


class BeToevoegenBoeking(FlaskForm):
    gast = SelectField('Selecteer gast', validate_choice=True)
    huis = SelectField('Selecteer woning', validate_choice=False)
    week = IntegerField('Kies week', validators=[InputRequired(), NumberRange(1, 52, 'weeknummer buiten bereik')])
    submit = SubmitField('Submit')


class BeToevoegenHuis(FlaskForm):
    naam = StringField('Naam van de nieuwe woning', validators=[InputRequired()])
    huisType = SelectField('Selecteer type', validate_choice=False)
    submit = SubmitField('Submit')


class BeToevoegenTypes(FlaskForm):
    idType = StringField('Naam van het type woning', validators=[InputRequired()])
    capaciteit = IntegerField('Capaciteit van de woning', validators=[NumberRange(1, 25, 'capaciteit niet reeel')])
    weekprijs = FloatField('Weekprijs accomodatie', validators=[InputRequired()])
    submit = SubmitField('submit')


class BeToevoegenGast(FlaskForm):
    email = EmailField('Account (emailadres)')
    wachtwoord = StringField('Tijdelijk wachtwoord')  # TODO: tijdelijk wachtwoord laten vervangen door gebruiker
    submit = SubmitField('submit')


class BeVerwijderenBoeking(FlaskForm):
    boeking = SelectField('selecteer boeking')
    submit = SubmitField('verwijder')


class BeVerwijderenGast(FlaskForm):
    gast = SelectField('selecteer gast')
    submit = SubmitField('verwijder')


class BeVerwijderenHuis(FlaskForm):
    huis = SelectField('selecteer huis')
    submit = SubmitField('verwijder')


class BeVerwijderenTypes(FlaskForm):
    types = SelectField('selecteer woning type')
    submit = SubmitField('verwijder')
