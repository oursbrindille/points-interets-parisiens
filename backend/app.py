from flask import Flask, render_template, request, jsonify,redirect
from flask_cors import CORS
import yaml
from database import db
import collections

app = Flask(__name__)
db_config = yaml.load(open('database.yaml'))
app.config['SQLALCHEMY_DATABASE_URI'] = db_config['uri']
db.init_app(app)

CORS(app)

from classes.userinfo import UserInfo
from classes.instanceobjectuser import InstanceObjectUser
from classes.evenement import Evenement
from classes.lieu import Lieu
from classes.roi import Roi
from classes.personnage import Personnage



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
    start = None
    end = None
    rois = getroijson(year,start,end)
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
        form = form+"<input type='hidden' name='urlimage' value=\""+str(row['urlimage'])+"\"/>&nbsp;&nbsp;"
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
        
    if(body['urlimage'] == "None"):
        editData.urlimage = None
    else:
        editData.urlimage = body['urlimage']

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
        urlimage = body['urlimage']

        data = Roi(wikiid,nom,dateofbirth,placeofbirthlabel,dateofdeath,placeofdeathlabel,mannersofdeath,placeofburiallabel,fatherlabel,motherlabel,spouses,starttime,endtime,startyear,endyear,birthyear,deathyear,urlimage)
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
            'deathyear': deathyear,
            'urlimage': urlimage

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
            'deathyear': str(data[i]).split('/')[17],
            'urlimage': str(data[i]).split('/')[18]
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
            'deathyear': str(data).split('/')[17],
            'urlimage': str(data).split('/')[18]
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
        editData.urlimage = body['urlimage']

        db.session.commit()
        return jsonify({'status': 'Data '+id+' is updated from PostgreSQL!'})


@app.route('/evenement/edit', methods=['GET'], defaults={'start': None, 'end': None})
@app.route('/evenement/edit/start/<start>/end/<end>', methods=['GET'])
def editevenement(start, end):
    if((start == None) & (end == None)):
        data = Evenement.query.order_by(Evenement.id_event).all()
    else:
        data = Evenement.query.order_by(Evenement.startyear).filter(Evenement.startyear>start, Evenement.startyear<end).all()
    columns = ['id_event','evenement','startyear','endyear','commentaire']
    evenements = getobjectsjson(data, columns)

    html = "<p>"+str(len(evenements))+"</p>"
    for row in evenements:
        form = "<form action='/evenement/form/update'>"
        form = form+"<input name='id_event' value=\""+str(row['id_event'])+"\"/>&nbsp;&nbsp;"
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
    for key in body:
        print(key)
        if(body[key] == "None"):
            setattr(editData, key, None)
        else:
            setattr(editData, key, body[key])
    db.session.commit()
    return "440" #redirect("/evenement/edit", code=302)


@app.route('/evenement', methods=['POST', 'GET'], defaults={'start': None, 'end': None})
@app.route('/evenement/start/<start>/end/<end>', methods=['POST', 'GET'])
def evenement(start, end):
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        data = Evenement(body['evenement'], body['startyear'], body['endyear'], body['commentaire'])
        db.session.add(data)
        db.session.commit()
        body['status'] = "All good"
        return jsonify(body)
    
    # GET all data from database & sort by id
    if request.method == 'GET':
        if((start == None) & (end == None)):
            data = Evenement.query.order_by(Evenement.id_event).all()
        else:
            data = Evenement.query.order_by(Evenement.startyear).filter(Evenement.startyear>start, Evenement.startyear<end).all()
        columns = ['id_event','evenement','startyear','endyear','commentaire']
        evenements = getobjectsjson(data, columns)
        return jsonify(evenements)

@app.route('/evenement/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def oneevenement(id):
    columns = ['id_event','evenement','startyear','endyear','commentaire']

    # GET a specific data by id
    if request.method == 'GET':
        return getonegeneric("evenement", columns, id)
        
    # DELETE a data
    if request.method == 'DELETE':
        return delonegeneric("evenement", id)

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        return putonegeneric("evenement", columns, id, body)


####### GENERIC FUNCTIONS #######


def getonegeneric(type, columns, id):
    if(type == "evenement"): 
        data = Evenement.query.get(id)
    dataDict = {}
    j = 0
    for key in columns:
        dataDict[key] = str(data).split('/')[j]
        j = j + 1
    return jsonify(dataDict)

def delonegeneric(type, id):
    if(type == "evenement"):
        delData = Evenement.query.filter_by(id_event=id).first()
    db.session.delete(delData)
    db.session.commit()
    return jsonify({'status': 'Data '+id+' is deleted from PostgreSQL!'})

def putonegeneric(type, columns, id, body):
    if(type == "evenement"):
        editData = Evenement.query.filter_by(id_event=id).first()
    for key in body:
        editData[key] = body[key]
    db.session.commit()
    return jsonify({'status': 'Data '+id+' is updated from PostgreSQL!'})

def getobjectsjson(data, columns):
    dataJson = []
    for i in range(len(data)):
        dataDict = {}
        j = 0
        for key in columns:
            dataDict[key] = str(data[i]).split('/')[j]
            j = j + 1
        dataJson.append(dataDict)
    return dataJson


if __name__ == '__main__':
    app.debug = True
    app.run()
