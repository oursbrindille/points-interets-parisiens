from database import db

class UserInfo(db.Model):
    __tablename__ = "user_info"
    id_user = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(255))

    def __init__(self, pseudo):
        self.pseudo = pseudo
    
    def __repr__(self):
        return '%s/%s' % (self.id_user, self.pseudo)
