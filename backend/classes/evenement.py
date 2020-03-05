from database import db

class Evenement(db.Model):
    __tablename__ = "evenement"
    id_event = db.Column(db.Integer, primary_key=True)
    evenement = db.Column(db.String(255))
    startyear = db.Column(db.Float)
    endyear = db.Column(db.Float)
    commentaire = db.Column(db.String(255))

    def __init__(self, name, age):
        self.id_event = id_event
        self.evenement = evenement
        self.startyear = startyear
        self.endyear = endyear
        self.commentaire = commentaire
    
    def __repr__(self):
        return '%s/%s/%s/%s/%s' % (self.id_event, self.evenement, self.startyear, self.endyear, self.commentaire)
