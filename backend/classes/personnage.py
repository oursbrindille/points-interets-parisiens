from database import db

class Personnage(db.Model):
    __tablename__ = "personnage"
    id_personnage = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255))
    dateofbirth = db.Column(db.Date)
    placeofbirthlabel = db.Column(db.String(255))
    dateofdeath = db.Column(db.Date)
    placeofdeathlabel = db.Column(db.String(255))
    positions = db.Column(db.String(255))
    birthyear = db.Column(db.Float)
    deathyear = db.Column(db.Float)

    def __init__(self, nom, dateofbirth, placeofbirthlabel, dateofdeath, placeofdeathlabel, positions, birthyear, deathyear):
        self.nom = nom
        self.dateofbirth = dateofbirth
        self.placeofbirthlabel = placeofbirthlabel
        self.dateofdeath = dateofdeath
        self.placeofdeathlabel = placeofdeathlabel
        self.positions = positions
        self.birthyear = birthyear
        self.deathyear = deathyear
    
    def __repr__(self):
        return '%s/%s/%s/%s/%s/%s/%s/%s/%s' % (self.id_personnage,self.nom,self.dateofbirth,self.placeofbirthlabel,self.dateofdeath,self.placeofdeathlabel,self.positions,self.birthyear,self.deathyear)

