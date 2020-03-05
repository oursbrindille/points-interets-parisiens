from database import db

class Roi(db.Model):
    __tablename__ = "roi"
    id_roi = db.Column(db.Integer, primary_key=True)
    wikiid = db.Column(db.String(255))
    nom = db.Column(db.String(255))
    dateofbirth = db.Column(db.Date)
    placeofbirthlabel = db.Column(db.String(255))
    dateofdeath = db.Column(db.Date)
    placeofdeathlabel = db.Column(db.String(255))
    mannersofdeath = db.Column(db.String(255))
    placeofburiallabel = db.Column(db.String(255))
    fatherlabel = db.Column(db.String(255))
    motherlabel = db.Column(db.String(255))
    spouses = db.Column(db.String(255))
    starttime = db.Column(db.Date)
    endtime = db.Column(db.Date)
    startyear = db.Column(db.Float)
    endyear = db.Column(db.Float)
    birthyear = db.Column(db.Float)
    deathyear = db.Column(db.Float)
    urlimage = db.Column(db.String(255))

    def __init__(self, name, age):
        self.id_roi = id_roi
        self.wikiid = wikiid
        self.nom = nom
        self.dateofbirth = dateofbirth
        self.placeofbirthlabel = placeofbirthlabel
        self.dateofdeath = dateofdeath
        self.placeofdeathlabel = placeofdeathlabel
        self.mannersofdeath = mannersofdeath
        self.placeofburiallabel = placeofburiallabel
        self.fatherlabel = fatherlabel
        self.motherlabel = motherlabel
        self.spouses = spouses
        self.starttime = starttime
        self.endtime = endtime
        self.startyear = startyear
        self.endyear = endyear
        self.birthyear = birthyear
        self.deathyear = deathyear
        self.urlimage = urlimage
    
    def __repr__(self):
        return '%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s' % (self.id_roi,self.wikiid,self.nom,self.dateofbirth,self.placeofbirthlabel,self.dateofdeath,self.placeofdeathlabel,self.mannersofdeath,self.placeofburiallabel,self.fatherlabel,self.motherlabel,self.spouses,self.starttime,self.endtime,self.startyear,self.endyear,self.birthyear,self.deathyear,self.urlimage)
