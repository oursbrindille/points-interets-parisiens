from flask import Flask, render_template, request, jsonify,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import yaml
import random

app = Flask(__name__)
db_config = yaml.load(open('database.yaml'))
app.config['SQLALCHEMY_DATABASE_URI'] = db_config['uri']
db = SQLAlchemy(app)
CORS(app)

@app.route('/')
def index():
    return "Background Jobs"

class InstanceObject(db.Model):
    __tablename__ = "instance_object"
    id_instance_object = db.Column(db.Integer, primary_key=True)
    id_external_object = db.Column(db.Integer)
    type_object = db.Column(db.String(255))
    lon = db.Column(db.Float)
    lat = db.Column(db.Float)

    def __init__(self, id_external_object, type_object, lon, lat):
        self.id_external_object = id_external_object
        self.type_object = type_object
        self.lon = lon
        self.lat = lat
    
    def __repr__(self):
        return '%s/%s/%s/%s/%s' % (self.id_instance_object, self.id_external_object, self.type_object, self.lon, self.lat)

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
    
    def __repr__(self):
        return '%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s' % (self.id_roi,self.wikiid,self.nom,self.dateofbirth,self.placeofbirthlabel,self.dateofdeath,self.placeofdeathlabel,self.mannersofdeath,self.placeofburiallabel,self.fatherlabel,self.motherlabel,self.spouses,self.starttime,self.endtime,self.startyear,self.endyear,self.birthyear,self.deathyear)


def genlat():
    rand = random.random()
    lat = (48.903767 - 48.811945)*rand+48.811945
    return "%.6f" %lat

def genlon():
    rand = random.random()
    lon = (2.416740 - 2.251700)*rand+2.251700
    return "%.6f" %lon


@app.route('/roi')
def getrois():
    rois = getroijson(500,600)
    return jsonify(rois[2])

@app.route('/generate')
def generate():
    instances = getinstanceobjectjson()
    rois = getroijson(500,600)
    evenements = getevenementjson(500,600)
    personnages = getpersonnagejson(500,600)

    html = ""
    for instance in instances:
        delData = InstanceObject.query.filter_by(id_instance_object=instance["id_instance_object"]).first()
        db.session.delete(delData)
        db.session.commit()

    for i in range(100):
        r = random.random()
        if(r < 0.33):
            data = InstanceObject(rois[random.randint(0,len(rois)-1)]['id_roi'], "roi", genlon(), genlat())
        if((r >=0.33) & (r < 0.66)):
            data = InstanceObject(evenements[random.randint(0,len(evenements)-1)]['id_event'], "evenement", genlon(), genlat())
        if(r >=0.66):
            data = InstanceObject(personnages[random.randint(0,len(personnages)-1)]['id_personnage'], "personnage", genlon(), genlat())

        db.session.add(data)
        db.session.commit()
    
    instances = getinstanceobjectjson()
    return jsonify(instances)

@app.route('/instances', methods=['POST', 'GET'])
def instances():
    
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        id_roi = body['id_roi']
        lon = body['lon']
        lat = body['lat']

        data = InstanceRoi(id_roi, lon, lat)
        db.session.add(data)
        db.session.commit()

        return jsonify({
            'status': 'Data is posted to PostgreSQL!',
            'id_roi': id_roi,
            'lon': lon,
            'lat': lat
        })
    
    # GET all data from database & sort by id
    if request.method == 'GET':
        instances = getinstanceobjectjson()
        return jsonify(instances)

def getinstanceobjectjson():
    # data = User.query.all()
    data = InstanceObject.query.order_by(InstanceObject.id_instance_object).all()
    print(data)
    dataJson = []
    for i in range(len(data)):
        # print(str(data[i]).split('/'))
        dataDict = {
            'id_instance_object': str(data[i]).split('/')[0],
            'id_external_object': str(data[i]).split('/')[1],
            'type_object': str(data[i]).split('/')[2],
            'lon': str(data[i]).split('/')[3],
            'lat': str(data[i]).split('/')[4]
        }
        dataJson.append(dataDict)
    return dataJson


def getroijson(start, end):
    # data = User.query.all()
    data = Roi.query.filter(Roi.startyear>=start, Roi.startyear<=end).order_by(Roi.startyear).all()
    #data = Roi.query.filter_by(startyear=None).all()
    
    dataJson = []
    for i in range(len(data)):
        # print(str(data[i]).split('/'))
        dataDict = {
            'id_roi': str(data[i]).split('/')[0],
            'wikiid': str(data[i]).split('/')[1],
            'nom': str(data[i]).split('/')[2],
            'dateofbirth': str(data[i]).split('/')[3],
            'placeofbirthlabel': str(data[i]).split('/')[4],
            'dateofdeath': str(data[i]).split('/')[5],
            'placeofdeathlabel': str(data[i]).split('/')[6],
            'mannersofdeath': str(data[i]).split('/')[7],
            'placeofburiallabel': str(data[i]).split('/')[8],
            'fatherlabel': str(data[i]).split('/')[9],
            'motherlabel': str(data[i]).split('/')[10],
            'spouses': str(data[i]).split('/')[11],
            'starttime': str(data[i]).split('/')[12],
            'endtime': str(data[i]).split('/')[13],
            'startyear': str(data[i]).split('/')[14],
            'endyear': str(data[i]).split('/')[15],
            'birthyear': str(data[i]).split('/')[16],
            'deathyear': str(data[i]).split('/')[17]
        }
        dataJson.append(dataDict)
    return dataJson

def getevenementjson(start, end):
    # data = User.query.all()
    if((start == None) & (end == None)):
        data = Evenement.query.order_by(Evenement.id_event).all()
    else:
        data = Evenement.query.order_by(Evenement.id_event).filter(Evenement.startyear>start, Evenement.startyear<end).all()
    print(data)
    dataJson = []
    for i in range(len(data)):
        # print(str(data[i]).split('/'))
        dataDict = {
            'id_event': str(data[i]).split('/')[0],
            'evenement': str(data[i]).split('/')[1],
            'startyear': str(data[i]).split('/')[2],
            'endyear': str(data[i]).split('/')[3],
            'commentaire': str(data[i]).split('/')[4]
        }
        dataJson.append(dataDict)
    return dataJson


def getpersonnagejson(start, end):
    # data = User.query.all()
    if((start == None) & (end == None)):
        data = Personnage.query.order_by(Personnage.birthyear).all()
    else:
        data = Personnage.query.filter(Personnage.birthyear>=start, Personnage.birthyear<=end).order_by(Personnage.birthyear).all()

    print(data)
    dataJson = []
    for i in range(len(data)):
        # print(str(data[i]).split('/'))
        dataDict = {
            'id_personnage': str(data[i]).split('/')[0],
            'nom': str(data[i]).split('/')[1],
            'dateofbirth': str(data[i]).split('/')[2],
            'placeofbirthlabel': str(data[i]).split('/')[3],
            'dateofdeath': str(data[i]).split('/')[4],
            'placeofdeathlabel': str(data[i]).split('/')[5],
            'positions': str(data[i]).split('/')[6],
            'birthyear': str(data[i]).split('/')[7],
            'deathyear': str(data[i]).split('/')[8]
        }
        dataJson.append(dataDict)
    return dataJson

if __name__ == '__main__':
    app.debug = True
    app.run(port=5001)