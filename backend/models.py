from app import db

class Event(db.Model):
    __tablename__ = 'evenement'

    id_event = Column(Integer, primary_key=True)
    evenement = Column(String)
    startyear = Column(Float)
    endyear = Column(Float)
    commentaire = Column(String)

    def __init__(self, name, author, published):
        self.id_event = id_event
        self.evenement = evenement
        self.startyear = startyear
        self.endyear = endyear
        self.commentaire = commentaire

    def __repr__(self):
        return '<id_event {}>'.format(self.id_event)

    def serialize(self):
        return {
            'id_event': self.id_event, 
            'evenement': self.evenement,
            'startyear': self.startyear,
            'endyear':self.endyear,
            'commentaire':self.commentaire
        }
