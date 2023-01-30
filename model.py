from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Hanze12345@localhost/zeeenduin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Huis(db.Model):
    
    __tablename__ = 'huis'
    
    naam = db.Column(db.Text, primary_key=True)
    huistype = db.Column(db.Text, db.ForeignKey('types.idType'))
    
    hboekingen = db.relationship('Boeking', backref='b_huis', lazy=True)
    # htype = db.relationship('types', backref='htype', uselist=False)

    def __repr__(self):
        return f"Villa {self.naam} is van type {self.huistype}"
    
class Boeking(db.Model):
    __tablename__ = 'boeking'
    idboeking = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gast = db.Column(db.Text, db.ForeignKey('gast.email'))
    huis = db.Column(db.Text, db.ForeignKey('huis.naam'))
    week = db.Column(db.Integer)
    
    # mijngast = db.relationship('gast', backref='email', uselist=False)
    
    def __repr__(self):
        return f'Boeking: {self.idboeking}, huis: {self.huis}, week: {self.week}'
        

class Gast(db.Model):
    __tablename__ = 'gast'
    email = db.Column(db.Text, primary_key=True)
    wachtwoord = db.Column(db.Text)
    
    gboekingen = db.relationship('Boeking', backref='b_gast', lazy=True)
    

class Types(db.Model):
    __tablename__ = 'types'
    idType = db.Column(db.Text, primary_key=True)
    capaciteit = db.Column(db.Integer)
    weekprijs = db.Column(db.Float)
    
    thuizen = db.relationship('Huis', backref='h_types', lazy=True)
    
    
with app.app_context():
    db.create_all()
    