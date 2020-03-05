
from database import db

class Lieu(db.Model):
    __tablename__ = "lieu"
    id_lieu = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255))
    lon = db.Column(db.Float)
    lat = db.Column(db.Float)
    inception = db.Column(db.String(255))
    constructionyear = db.Column(db.Float)

    def __init__(self, name, age):
        self.id_lieu = id_lieu
        self.nom = nom
        self.lon = lon
        self.lat = lat
        self.inception = inception
        self.constructionyear = constructionyear
    
    def __repr__(self):
        return '%s/%s/%s/%s/%s/%s' % (self.id_lieu, self.nom, self.lon, self.lat, self.inception,self.constructionyear)

