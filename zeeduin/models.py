from zeeduin import db

class Huis(db.Model):
    __tablename__ = 'huis'
    
    naam = db.Column(db.Text, primary_key=True)
    huistype = db.Column(db.Text, db.ForeignKey('types.idType'))
    
    boekingen = db.relationship('Boeking', backref='bhuis', lazy=True)
    
    def __repr__(self):
        return f"Villa {self.naam} is van type {self.huistype}"


class Boeking(db.Model):
    __tablename__ = 'boeking'
    idboeking = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gast = db.Column(db.Text, db.ForeignKey('gast.email'))
    huis = db.Column(db.Text, db.ForeignKey('huis.naam'))
    week = db.Column(db.Integer)
    
    def __repr__(self):
        return f'Boeking: {self.idboeking}, huis: {self.huis}, week: {self.week}'


class Gast(db.Model):
    __tablename__ = 'gast'
    email = db.Column(db.Text, primary_key=True)
    wachtwoord = db.Column(db.Text)
    
    boekingen = db.relationship('Boeking', backref='bgast', lazy=True)


class Types(db.Model):
    __tablename__ = 'types'
    idType = db.Column(db.Text, primary_key=True)
    capaciteit = db.Column(db.Integer)
    weekprijs = db.Column(db.Float)
    
    huizen = db.relationship('Huis', backref='types', lazy=True)


class Staf(db.Model):
    __tablename__ = 'staf'
    email = db.Column(db.Text, primary_key=True)
    wachtwoord = db.Column(db.Text)


# db.create_all()
