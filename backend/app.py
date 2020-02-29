from flask import Flask, render_template, request, jsonify,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import yaml

app = Flask(__name__)
db_config = yaml.load(open('database.yaml'))
app.config['SQLALCHEMY_DATABASE_URI'] = db_config['uri']
db = SQLAlchemy(app)

CORS(app)

class UserInfo(db.Model):
    __tablename__ = "user_info"
    id_user = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(255))

    def __init__(self, pseudo):
        self.pseudo = pseudo
    
    def __repr__(self):
        return '%s/%s' % (self.id_user, self.pseudo)


class InstanceObjectUser(db.Model):
    __tablename__ = "instance_object_user"
    id_instance_object_user = db.Column(db.Integer, primary_key=True)
    id_external_object = db.Column(db.Integer)
    id_user = db.Column(db.Integer)
    type_object = db.Column(db.String(255))
    lon = db.Column(db.Float)
    lat = db.Column(db.Float)

    def __init__(self, id_external_object, id_user, type_object, lon, lat):
        self.id_external_object = id_external_object
        self.id_user = id_user
        self.type_object = type_object
        self.lon = lon
        self.lat = lat
    
    def __repr__(self):
        return '%s/%s/%s/%s/%s/%s' % (self.id_instance_object_user, self.id_external_object, self.id_user, self.type_object, self.lon, self.lat)


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


@app.route('/')
def index():
    return render_template('home.html')



@app.route('/user', methods=['POST', 'GET'])
def user():
    
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        pseudo = body['pseudo']

        data = UserInfo(pseudo)
        db.session.add(data)
        db.session.commit()

        return jsonify({
            'status': 'Data is posted to PostgreSQL!',
            'pseudo': pseudo
        })
    
    # GET all data from database & sort by id
    if request.method == 'GET':
        users = getuserjson()
        return jsonify(users)

def getuserjson():
    # data = User.query.all()
    data = UserInfo.query.order_by(UserInfo.id_user).all()
    print(data)
    dataJson = []
    for i in range(len(data)):
        # print(str(data[i]).split('/'))
        dataDict = {
            'id_user': str(data[i]).split('/')[0],
            'pseudo': str(data[i]).split('/')[1]
        }
        dataJson.append(dataDict)
    return dataJson

@app.route('/user/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def oneuser(id):

    # GET a specific data by id
    if request.method == 'GET':
        data = UserInfo.query.get(id)
        print(data)
        dataDict = {
            'id_user': str(data).split('/')[0],
            'pseudo': str(data).split('/')[1]
        }
        return jsonify(dataDict)
        
    # DELETE a data
    if request.method == 'DELETE':
        delData = UserInfo.query.filter_by(id_user=id).first()
        db.session.delete(delData)
        db.session.commit()
        return jsonify({'status': 'Data '+id+' is deleted from PostgreSQL!'})

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        editData = UserInfo.query.filter_by(id_user=id).first()
        editData.nom = body['pseudo']
        db.session.commit()
        return jsonify({'status': 'Data '+id+' is updated from PostgreSQL!'})



@app.route('/instance-user', methods=['POST', 'GET'], defaults={'userid': None})
@app.route('/instance-user/user/<string:userid>', methods=['POST', 'GET'])
def instanceuser(userid):
    
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        id_external_object = body['id_external_object']
        id_user = body['id_user']
        type_object = body['type_object']
        lon = body['lon']
        lat = body['lat']

        data = InstanceObjectUser(id_external_object, id_user, type_object, lon, lat)
        db.session.add(data)
        db.session.commit()

        return jsonify({
            'status': 'Data is posted to PostgreSQL!',
            'id_external_object': id_external_object,
            'id_user': id_user,
            'type_object': type_object,
            'lon': lon,
            'lat': lat
        })
    
    # GET all data from database & sort by id
    if request.method == 'GET':
        instances = getinstanceuserjson(userid)
        return jsonify(instances)

def getinstanceuserjson(userid):
    # data = User.query.all()
    if(userid == None):
        data = InstanceObjectUser.query.order_by(InstanceObjectUser.id_instance_object_user).all()
    else:
        data = InstanceObjectUser.query.filter_by(id_user=userid).order_by(InstanceObjectUser.id_instance_object_user).all()
    print(data)
    dataJson = []
    for i in range(len(data)):
        # print(str(data[i]).split('/'))
        dataDict = {
            'id_instance_object_user': str(data[i]).split('/')[0],
            'id_external_object': str(data[i]).split('/')[1],
            'id_user': str(data[i]).split('/')[2],
            'type_object': str(data[i]).split('/')[3],
            'lon': str(data[i]).split('/')[4],
            'lat': str(data[i]).split('/')[5]
        }
        dataJson.append(dataDict)
    return dataJson




@app.route('/lieu/edit', methods=['GET'])
def editlieu():
    lieux = getlieujson()
    html = "<p>"+str(len(lieux))+"</p>"
    for row in lieux:
        form = "<form action='/lieu/form/update'>"
        form = form+"<input type='hidden' name='id_lieu' value=\""+str(row['id_lieu'])+"\"/>&nbsp;&nbsp;"
        form = form+"<textarea name='nom' rows='3' cols='50'>"+str(row['nom'])+"</textarea>&nbsp;&nbsp;"
        form = form+"<input size='5' name='lon' value=\""+str(row['lon'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='lat' value=\""+str(row['lat'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='inception' value=\""+str(row['inception'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='constructionyear' value=\""+str(row['constructionyear'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input type='submit' name='button' value='Supprimer'>&nbsp;&nbsp;"
        form = form+"<input type='submit' name='button' value='Valider'></form>"
        html = html+form    
    return html

@app.route('/lieu/form/update', methods=['POST', 'GET'])
def updatelieu():
    body = request.values
    editData = Lieu.query.filter_by(id_lieu=body['id_lieu']).first()
    if(body['nom'] == "None"):
        editData.nom = None
    else:
        editData.nom = body['nom']

    if(body['lon'] == "None"):
        editData.lon = None
    else:
        editData.lon = body['lon']

    if(body['lat'] == "None"):
        editData.lat = None
    else:
        editData.lat = body['lat']
        
    if(body['inception'] == "None"):
        editData.inception = None
    else:
        editData.inception = body['inception']
        
    if(body['constructionyear'] == "None"):
        editData.constructionyear = None
    else:
        editData.constructionyear = body['constructionyear']

    db.session.commit()
    return redirect("/lieu/edit", code=302)


@app.route('/lieu', methods=['POST', 'GET'])
def lieu():
    
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        nom = body['nom']
        lon = body['lon']
        lat = body['lat']
        inception = body['inception']
        constructionyear = body['constructionyear']

        data = Lieu(nom, lon, lat, inception, constructionyear)
        db.session.add(data)
        db.session.commit()

        return jsonify({
            'status': 'Data is posted to PostgreSQL!',
            'nom': nom,
            'lon': lon,
            'lat': lat,
            'inception': inception,
            'constructionyear': constructionyear
        })
    
    # GET all data from database & sort by id
    if request.method == 'GET':
        lieux = getlieujson()
        return jsonify(lieux)

def getlieujson():
    # data = User.query.all()
    data = Lieu.query.order_by(Lieu.id_lieu).all()
    print(data)
    dataJson = []
    for i in range(len(data)):
        # print(str(data[i]).split('/'))
        dataDict = {
            'id_lieu': str(data[i]).split('/')[0],
            'nom': str(data[i]).split('/')[1],
            'lon': str(data[i]).split('/')[2],
            'lat': str(data[i]).split('/')[3],
            'inception': str(data[i]).split('/')[4],
            'constructionyear': str(data[i]).split('/')[5]
        }
        dataJson.append(dataDict)
    return dataJson

@app.route('/lieu/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onelieu(id):

    # GET a specific data by id
    if request.method == 'GET':
        data = Lieu.query.get(id)
        print(data)
        dataDict = {
            'id_lieu': str(data).split('/')[0],
            'nom': str(data).split('/')[1],
            'lon': str(data).split('/')[2],
            'lat': str(data).split('/')[3],
            'inception': str(data).split('/')[4],
            'constructionyear': str(data).split('/')[5]
        }
        return jsonify(dataDict)
        
    # DELETE a data
    if request.method == 'DELETE':
        delData = Lieu.query.filter_by(id_lieu=id).first()
        db.session.delete(delData)
        db.session.commit()
        return jsonify({'status': 'Data '+id+' is deleted from PostgreSQL!'})

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        editData = Lieu.query.filter_by(id_lieu=id).first()
        editData.nom = body['nom']
        editData.lon = body['lon']
        editData.lat = body['lat']
        editData.inception = body['inception']
        editData.constructionyear = body['constructionyear']
        db.session.commit()
        return jsonify({'status': 'Data '+id+' is updated from PostgreSQL!'})








@app.route('/personnage/edit', methods=['GET'], defaults={'start': None, 'end': None})
@app.route('/personnage/edit/start/<start>/end/<end>', methods=['GET'])
def editpersonnage(start, end):
    personnages = getpersonnagejson(start, end)
    html = ""
    for row in personnages:
        form = "<form action='/personnage/form/update'>"
        form = form+"<input type='hidden' name='id_personnage' value=\""+str(row['id_personnage'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='20' name='nom' value=\""+str(row['nom'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='dateofbirth' value=\""+str(row['dateofbirth'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='placeofbirthlabel' value=\""+str(row['placeofbirthlabel'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='dateofdeath' value=\""+str(row['dateofdeath'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='placeofdeathlabel' value=\""+str(row['placeofdeathlabel'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='positions' value=\""+str(row['positions'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='birthyear' value=\""+str(row['birthyear'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='deathyear' value=\""+str(row['deathyear'])+"\"/>&nbsp;&nbsp;"  
        form = form+"<input type='submit' name='button' value='Valider'></form>"
        html = html+form 
    
    form = "<form action='/personnage/form/create'>"
    form = form+"<input size='20' name='nom' value=''/>&nbsp;&nbsp;"
    form = form+"<input size='10' name='dateofbirth' value=''/>&nbsp;&nbsp;"
    form = form+"<input size='10' name='placeofbirthlabel' value=''/>&nbsp;&nbsp;"
    form = form+"<input size='10' name='dateofdeath' value=''/>&nbsp;&nbsp;"
    form = form+"<input size='10' name='placeofdeathlabel' value=''/>&nbsp;&nbsp;"
    form = form+"<input size='10' name='positions' value=''/>&nbsp;&nbsp;"
    form = form+"<input size='5' name='birthyear' value=''/>&nbsp;&nbsp;"
    form = form+"<input size='5' name='deathyear' value=''/>&nbsp;&nbsp;"  
    form = form+"<input type='submit' name='button' value='Ajouter'></form>"
    html = html+form
    return html



@app.route('/personnage/form/create', methods=['POST','GET'])
def createpersonnage():
    body = request.values
    

    if(body['nom'] == "None"):
        nom = None
    else:
        nom = body['nom']
    
    if(body['dateofbirth'] == "None"):
        dateofbirth = None
    else:
        dateofbirth = body['dateofbirth']
    
    if(body['placeofbirthlabel'] == "None"):
        placeofbirthlabel = None
    else:
        placeofbirthlabel = body['placeofbirthlabel']
    
    if(body['dateofdeath'] == "None"):
        dateofdeath = None
    else:
        dateofdeath = body['dateofdeath']
    
    if(body['placeofdeathlabel'] == "None"):
        placeofdeathlabel = None
    else:
        placeofdeathlabel = body['placeofdeathlabel']
    
    if(body['positions'] == "None"):
        positions = None
    else:
        positions = body['positions']
    
    if(body['birthyear'] == "None"):
        birthyear = None
    else:
        birthyear = body['birthyear']
    
    if(body['deathyear'] == "None"):
        deathyear = None
    else:
        deathyear = body['deathyear']

    data = Personnage(nom,dateofbirth,placeofbirthlabel,dateofdeath,placeofdeathlabel,positions,birthyear,deathyear)
    db.session.add(data)
    db.session.commit()
    return redirect("/personnage/edit", code=302)


@app.route('/personnage/form/update', methods=['POST', 'GET'])
def updatepersonnage():
    body = request.values
    print("toto")
    editData = Personnage.query.filter_by(id_personnage=body['id_personnage']).first()
    
    if(body['nom'] == "None"):
        editData.nom = None
    else:
        editData.nom = body['nom']
    
    if(body['dateofbirth'] == "None"):
        editData.dateofbirth = None
    else:
        editData.dateofbirth = body['dateofbirth']
    
    if(body['placeofbirthlabel'] == "None"):
        editData.placeofbirthlabel = None
    else:
        editData.placeofbirthlabel = body['placeofbirthlabel']
    
    if(body['dateofdeath'] == "None"):
        editData.dateofdeath = None
    else:
        editData.dateofdeath = body['dateofdeath']
    
    if(body['placeofdeathlabel'] == "None"):
        editData.placeofdeathlabel = None
    else:
        editData.placeofdeathlabel = body['placeofdeathlabel']
    
    if(body['positions'] == "None"):
        editData.positions = None
    else:
        editData.positions = body['positions']
    
    if(body['birthyear'] == "None"):
        editData.birthyear = None
    else:
        editData.birthyear = body['birthyear']
    
    if(body['deathyear'] == "None"):
        editData.deathyear = None
    else:
        editData.deathyear = body['deathyear']
    
    db.session.commit()
    return redirect("/personnage/edit", code=302)


@app.route('/personnage', methods=['POST', 'GET'], defaults={'start': None, 'end': None})
@app.route('/personnage/start/<start>/end/<end>', methods=['POST', 'GET'])
def personnage(start, end):
    
    # POST a data to database
    if request.method == 'POST':
        body = request.json

        nom = body['nom']
        dateofbirth = body['dateofbirth']
        placeofbirthlabel = body['placeofbirthlabel']
        dateofdeath = body['dateofdeath']
        placeofdeathlabel = body['placeofdeathlabel']
        positions = body['positions']
        birthyear = body['birthyear']
        deathyear = body['deathyear']

        data = Roi(nom,dateofbirth,placeofbirthlabel,dateofdeath,placeofdeathlabel,positions,birthyear,deathyear)
        db.session.add(data)
        db.session.commit()

        return jsonify({
            'status': 'Data is posted to PostgreSQL!',
   
            'nom': nom,
            'dateofbirth': dateofbirth,
            'placeofbirthlabel': placeofbirthlabel,
            'dateofdeath': dateofdeath,
            'placeofdeathlabel': placeofdeathlabel,
            'positions': positions,
            'birthyear': birthyear,
            'deathyear': deathyear

        })
    
    # GET all data from database & sort by id
    if request.method == 'GET':
        personnages = getpersonnagejson(start, end)
        return jsonify(personnages)

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

@app.route('/personnage/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onepersonnage(id):

    # GET a specific data by id
    if request.method == 'GET':
        data = Personnage.query.get(id)
        print("dddd ==> ")
        print(data)
        dataDict = {
            'id_personnage': str(data).split('/')[0],
            'nom': str(data).split('/')[1],
            'dateofbirth': str(data).split('/')[2],
            'placeofbirthlabel': str(data).split('/')[3],
            'dateofdeath': str(data).split('/')[4],
            'placeofdeathlabel': str(data).split('/')[5],
            'positions': str(data).split('/')[6],
            'birthyear': str(data).split('/')[7],
            'deathyear': str(data).split('/')[8]
        }
        
        return jsonify(dataDict)
        
    # DELETE a data
    if request.method == 'DELETE':
        delData = Personnage.query.filter_by(id_personnage=id).first()
        db.session.delete(delData)
        db.session.commit()
        return jsonify({'status': 'Data '+id+' is deleted from PostgreSQL!'})

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        editData = Personnage.query.filter_by(id_personnage=id).first()
        editData.nom = body['nom']
        editData.dateofbirth = body['dateofbirth']
        editData.placeofbirthlabel = body['placeofbirthlabel']
        editData.dateofdeath = body['dateofdeath']
        editData.placeofdeathlabel = body['placeofdeathlabel']
        editData.positions = body['positions']
        editData.birthyear = body['birthyear']
        editData.deathyear = body['deathyear']

        db.session.commit()
        return jsonify({'status': 'Data '+id+' is updated from PostgreSQL!'})

















@app.route('/roi/edit', methods=['GET'])
def editroi():
    year = None
    rois = getroijson(year)
    html = ""
    for row in rois:
        form = "<form action='/roi/form/update'>"
        form = form+"<input type='hidden' name='id_roi' value=\""+str(row['id_roi'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input type='hidden' name='wikiid' value=\""+str(row['wikiid'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='nom' value=\""+str(row['nom'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='dateofbirth' value=\""+str(row['dateofbirth'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='placeofbirthlabel' value=\""+str(row['placeofbirthlabel'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='dateofdeath' value=\""+str(row['dateofdeath'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='placeofdeathlabel' value=\""+str(row['placeofdeathlabel'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='mannersofdeath' value=\""+str(row['mannersofdeath'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='placeofburiallabel' value=\""+str(row['placeofburiallabel'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='fatherlabel' value=\""+str(row['fatherlabel'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='motherlabel' value=\""+str(row['motherlabel'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='spouses' value=\""+str(row['spouses'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='starttime' value=\""+str(row['starttime'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='endtime' value=\""+str(row['endtime'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='startyear' value=\""+str(row['startyear'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='endyear' value=\""+str(row['endyear'])+"\"/>&nbsp;&nbsp;"  
        form = form+"<input size='5' name='birthyear' value=\""+str(row['birthyear'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='deathyear' value=\""+str(row['deathyear'])+"\"/>&nbsp;&nbsp;"  
        form = form+"<input type='submit' name='button' value='Supprimer'>&nbsp;&nbsp;"
        form = form+"<input type='submit' name='button' value='Valider'></form>"
        html = html+form 
    return html

@app.route('/roi/form/update', methods=['POST', 'GET'])
def updateroi():
    body = request.values
    print("toto")
    editData = Roi.query.filter_by(id_roi=body['id_roi']).first()

    if(body['wikiid'] == "None"):
        editData.wikiid = None
    else:
        editData.wikiid = body['wikiid']
    
    if(body['nom'] == "None"):
        editData.nom = None
    else:
        editData.nom = body['nom']
    
    if(body['dateofbirth'] == "None"):
        editData.dateofbirth = None
    else:
        editData.dateofbirth = body['dateofbirth']
    
    if(body['placeofbirthlabel'] == "None"):
        editData.placeofbirthlabel = None
    else:
        editData.placeofbirthlabel = body['placeofbirthlabel']
    
    if(body['dateofdeath'] == "None"):
        editData.dateofdeath = None
    else:
        editData.dateofdeath = body['dateofdeath']
    
    if(body['placeofdeathlabel'] == "None"):
        editData.placeofdeathlabel = None
    else:
        editData.placeofdeathlabel = body['placeofdeathlabel']
    
    if(body['mannersofdeath'] == "None"):
        editData.mannersofdeath = None
    else:
        editData.mannersofdeath = body['mannersofdeath']
    
    if(body['placeofburiallabel'] == "None"):
        editData.starttime = None
    else:
        editData.placeofburiallabel = body['placeofburiallabel']
    
    if(body['fatherlabel'] == "None"):
        editData.fatherlabel = None
    else:
        editData.fatherlabel = body['fatherlabel']
    
    if(body['motherlabel'] == "None"):
        editData.motherlabel = None
    else:
        editData.motherlabel = body['motherlabel']
    
    if(body['spouses'] == "None"):
        editData.spouses = None
    else:
        editData.spouses = body['spouses']
    
    if(body['starttime'] == "None"):
        editData.starttime = None
    else:
        editData.starttime = body['starttime']
    
    if(body['endtime'] == "None"):
        editData.endtime = None
    else:
        editData.endtime = body['endtime']
    
    if(body['startyear'] == "None"):
        editData.startyear = None
    else:
        editData.startyear = body['startyear']
    
    if(body['endyear'] == "None"):
        editData.endyear = None
    else:
        editData.endyear = body['endyear']
        
    if(body['birthyear'] == "None"):
        editData.birthyear = None
    else:
        editData.birthyear = body['birthyear']
        
    if(body['deathyear'] == "None"):
        editData.deathyear = None
    else:
        editData.deathyear = body['deathyear']
    if(body['button'] == 'Valider'):
        db.session.commit()
    if(body['button'] == 'Supprimer'):
        db.session.delete(editData)
        db.session.commit()
    return redirect("/roi/edit", code=302)


@app.route('/roi', methods=['POST', 'GET'], defaults={'year': None, 'start':None,'end':None})
@app.route('/roi/year/<year>', methods=['POST', 'GET'], defaults={'start':None,'end':None})
@app.route('/roi/start/<start>/end/<end>', methods=['POST', 'GET'], defaults={'year':None})
def roi(year, start, end):
    
    # POST a data to database
    if request.method == 'POST':
        body = request.json

        wikiid = body['wikiid']
        nom = body['nom']
        dateofbirth = body['dateofbirth']
        placeofbirthlabel = body['placeofbirthlabel']
        dateofdeath = body['dateofdeath']
        placeofdeathlabel = body['placeofdeathlabel']
        mannersofdeath = body['mannersofdeath']
        placeofburiallabel = body['placeofburiallabel']
        fatherlabel = body['fatherlabel']
        motherlabel = body['motherlabel']
        spouses = body['spouses']
        starttime = body['starttime']
        endtime = body['endtime']
        startyear = body['startyear']
        endyear = body['endyear']
        birthyear = body['birthyear']
        deathyear = body['deathyear']

        data = Roi(wikiid,nom,dateofbirth,placeofbirthlabel,dateofdeath,placeofdeathlabel,mannersofdeath,placeofburiallabel,fatherlabel,motherlabel,spouses,starttime,endtime,startyear,endyear,birthyear,deathyear)
        db.session.add(data)
        db.session.commit()

        return jsonify({
            'status': 'Data is posted to PostgreSQL!',
   
            'wikiid': wikiid,
            'nom': nom,
            'dateofbirth': dateofbirth,
            'placeofbirthlabel': placeofbirthlabel,
            'dateofdeath': dateofdeath,
            'placeofdeathlabel': placeofdeathlabel,
            'mannersofdeath': mannersofdeath,
            'placeofburiallabel': placeofburiallabel,
            'fatherlabel': fatherlabel,
            'motherlabel': motherlabel,
            'spouses': spouses,
            'starttime': starttime,
            'endtime': endtime,
            'startyear': startyear,
            'endyear': endyear,
            'birthyear': birthyear,
            'deathyear': deathyear

        })
    
    # GET all data from database & sort by id
    if request.method == 'GET':
        rois = getroijson(year, start, end)
        return jsonify(rois)

def getroijson(year, start, end):
    # data = User.query.all()
    if(year == None):
        if((start == None) & (end == None)):
            data = Roi.query.order_by(Roi.startyear).all()
        else:
            data = Roi.query.filter(Roi.startyear>=start, Roi.startyear<=end).order_by(Roi.startyear).all()
    else:
        data = Roi.query.filter(Roi.startyear<=year, Roi.endyear>=year).order_by(Roi.startyear).all()
    #data = Roi.query.filter_by(startyear=None).all()
    
    print(data)
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

@app.route('/roi/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def oneroi(id):

    # GET a specific data by id
    if request.method == 'GET':
        data = Roi.query.get(id)
        print("dddd ==> ")
        print(data)
        dataDict = {
            'id_roi': str(data).split('/')[0],
            'wikiid': str(data).split('/')[1],
            'nom': str(data).split('/')[2],
            'dateofbirth': str(data).split('/')[3],
            'placeofbirthlabel': str(data).split('/')[4],
            'dateofdeath': str(data).split('/')[5],
            'placeofdeathlabel': str(data).split('/')[6],
            'mannersofdeath': str(data).split('/')[7],
            'placeofburiallabel': str(data).split('/')[8],
            'fatherlabel': str(data).split('/')[9],
            'motherlabel': str(data).split('/')[10],
            'spouses': str(data).split('/')[11],
            'starttime': str(data).split('/')[12],
            'endtime': str(data).split('/')[13],
            'startyear': str(data).split('/')[14],
            'endyear': str(data).split('/')[15],
            'birthyear': str(data).split('/')[16],
            'deathyear': str(data).split('/')[17]
        }
        
        return jsonify(dataDict)
        
    # DELETE a data
    if request.method == 'DELETE':
        delData = Roi.query.filter_by(id_roi=id).first()
        db.session.delete(delData)
        db.session.commit()
        return jsonify({'status': 'Data '+id+' is deleted from PostgreSQL!'})

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        editData = Roi.query.filter_by(id_roi=id).first()
        editData.wikiid = body['wikiid']
        editData.nom = body['nom']
        editData.dateofbirth = body['dateofbirth']
        editData.placeofbirthlabel = body['placeofbirthlabel']
        editData.dateofdeath = body['dateofdeath']
        editData.placeofdeathlabel = body['placeofdeathlabel']
        editData.mannersofdeath = body['mannersofdeath']
        editData.placeofburiallabel = body['placeofburiallabel']
        editData.fatherlabel = body['fatherlabel']
        editData.motherlabel = body['motherlabel']
        editData.spouses = body['spouses']
        editData.starttime = body['starttime']
        editData.endtime = body['endtime']
        editData.startyear = body['startyear']
        editData.endyear = body['endyear']
        editData.birthyear = body['birthyear']
        editData.deathyear = body['deathyear']

        db.session.commit()
        return jsonify({'status': 'Data '+id+' is updated from PostgreSQL!'})


@app.route('/evenement/edit', methods=['GET'], defaults={'start': None, 'end': None})
@app.route('/evenement/edit/start/<start>/end/<end>', methods=['GET'])
def editevenement(start, end):
    evenements = getevenementjson(start,end)
    html = "<p>"+str(len(evenements))+"</p>"
    for row in evenements:
        form = "<form action='/evenement/form/update'>"
        form = form+"<input type='hidden' name='id_event' value=\""+str(row['id_event'])+"\"/>&nbsp;&nbsp;"
        form = form+"<textarea name='evenement' rows='3' cols='50'>"+str(row['evenement'])+"</textarea>&nbsp;&nbsp;"
        form = form+"<input size='5' name='startyear' value=\""+str(row['startyear'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='endyear' value=\""+str(row['endyear'])+"\"/>&nbsp;&nbsp;"
        form = form+"<textarea name='commentaire' rows='3' cols='50'>"+str(row['commentaire'])+"</textarea>&nbsp;&nbsp;"
        form = form+"<input type='submit' name='button' value='Supprimer'>&nbsp;&nbsp;"
        form = form+"<input type='submit' name='button' value='Valider'></form>"
        html = html+form    
    return html

@app.route('/evenement/form/update', methods=['POST', 'GET'])
def updateevenement():
    body = request.values
    editData = Evenement.query.filter_by(id_event=body['id_event']).first()
    if(body['evenement'] == "None"):
        editData.evenement = None
    else:
        editData.evenement = body['evenement']

    if(body['startyear'] == "None"):
        editData.startyear = None
    else:
        editData.startyear = body['startyear']

    if(body['endyear'] == "None"):
        editData.endyear = None
    else:
        editData.endyear = body['endyear']
        
    if(body['commentaire'] == "None"):
        editData.commentaire = None
    else:
        editData.commentaire = body['commentaire']

    db.session.commit()
    return redirect("/evenement/edit", code=302)


@app.route('/evenement', methods=['POST', 'GET'], defaults={'start': None, 'end': None})
@app.route('/evenement/start/<start>/end/<end>', methods=['POST', 'GET'])
def evenement(start, end):
    
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        evenement = body['evenement']
        startyear = body['startyear']
        endyear = body['endyear']
        commentaire = body['commentaire']

        data = Evenement(evenement, startyear, endyear, commentaire)
        db.session.add(data)
        db.session.commit()

        return jsonify({
            'status': 'Data is posted to PostgreSQL!',
            'evenemnent': evenement,
            'staryear': startyear,
            'endyear': endyear,
            'commentaire': commentaire
        })
    
    # GET all data from database & sort by id
    if request.method == 'GET':
        evenements = getevenementjson(start, end)
        return jsonify(evenements)

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

@app.route('/evenement/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def oneevenement(id):

    # GET a specific data by id
    if request.method == 'GET':
        data = Evenement.query.get(id)
        print(data)
        dataDict = {
            'id_event': str(data).split('/')[0],
            'evenement': str(data).split('/')[1],
            'startyear': str(data).split('/')[2],
            'endyear': str(data).split('/')[3],
            'commentaire': str(data).split('/')[4]
        }
        return jsonify(dataDict)
        
    # DELETE a data
    if request.method == 'DELETE':
        delData = Evenement.query.filter_by(id_event=id).first()
        db.session.delete(delData)
        db.session.commit()
        return jsonify({'status': 'Data '+id+' is deleted from PostgreSQL!'})

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        editData = Evenement.query.filter_by(id_event=id).first()
        editData.evenement = body['evenement']
        editData.startyear = body['startyear']
        editData.endyear = body['endyear']
        editData.commentaire = body['commentaire']
        db.session.commit()
        return jsonify({'status': 'Data '+id+' is updated from PostgreSQL!'})

if __name__ == '__main__':
    app.debug = True
    app.run()
