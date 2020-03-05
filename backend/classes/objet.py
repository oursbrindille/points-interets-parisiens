
from database import db

class Objet(db.Model):
    __tablename__ = "objet"
    id_objet = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255))
    startyear = db.Column(db.Float)
    endyear = db.Column(db.Float)
    prod = db.Column(db.Integer)

    def __init__(self, nom, startyear, endyear, prod):
        self.nom = nom
        self.startyear = startyear
        self.endyear = endyear
        self.prod = prod
    
    def __repr__(self):
        return '%s/%s/%s/%s/%s' % (self.id_objet, self.nom, self.startyear, self.endyear, self.prod)

