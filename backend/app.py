from flask import Flask, render_template, request, jsonify,redirect
from flask_cors import CORS
import yaml
from database import db
import random
from flask_sqlalchemy import SQLAlchemy


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
from classes.instanceobject import InstanceObject

columns_userinfo = ['id_user', 'pseudo']
columns_instanceobjectuser = ['id_instance_object_user', 'id_external_object','id_user','type_object','lon','lat']
columns_evenement = ['id_event','evenement','startyear','endyear','commentaire', 'prod']
columns_lieu = ['id_lieu','nom','lon','lat','inception', 'constructionyear', 'prod']
columns_roi = ['id_roi','wikiid','nom','dateofbirth','placeofbirthlabel', 'dateofdeath','placeofdeathlabel','mannersofdeath','placeofburiallabel','fatherlabel','motherlabel','spouses','starttime','endtime','startyear','endyear','birthyear','deathyear','urlimage', 'prod']
columns_personnage = ['id_personnage','nom','dateofbirth','placeofbirthlabel','dateofdeath', 'placeofdeathlabel','positions','birthyear','deathyear', 'prod']
columns_instanceobject = ['id_instance_object', 'id_external_object', 'type_object','lon','lat']


@app.route('/')
def index():
    return render_template('home.html')

################### USER ##############

@app.route('/user', methods=['POST', 'GET'])
def user():
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        data = InstanceObjectUser(body['pseudo'])
        db.session.add(data)
        db.session.commit()
        body['status'] = "All good"
        return jsonify(body)

    # GET all data from database & sort by id
    if request.method == 'GET':
        data = UserInfo.query.order_by(UserInfo.id_user).all()
        users = getobjectsjson(data, columns_userinfo)
        return jsonify(users)

@app.route('/user/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def oneuser(id):
    # GET a specific data by id
    if request.method == 'GET':
        return getonegeneric("user", columns_userinfo, id)
        
    # DELETE a data
    if request.method == 'DELETE':
        return delonegeneric("user", id)

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        return putonegeneric("user", columns_userinfo, id, body)


################ INSTANCE OBJECT ################


@app.route('/catch', methods=['POST', 'GET'], defaults={'userid': None})
@app.route('/catch/user/<string:userid>', methods=['POST', 'GET'])
def instanceuser(userid):
    
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        data = InstanceObjectUser(body['id_external_object'], body['id_user'], body['type_object'], body['lon'], body['lat'])
        db.session.add(data)
        db.session.commit()
        body['status'] = "All good"
        return jsonify(body)
    
    # GET all data from database & sort by id
    if request.method == 'GET':
        if(userid == None):
            data = InstanceObjectUser.query.order_by(InstanceObjectUser.id_instance_object_user).all()
        else:
            data = InstanceObjectUser.query.filter_by(id_user=userid).order_by(InstanceObjectUser.id_instance_object_user).all()
        instances = getobjectsjson(data, columns_instanceobjectuser)
        return jsonify(instances)

############ BEWARE SEP INSTANCES et INSTANCEUSER

@app.route('/instances/generate')
def generate():
    data = InstanceObject.query.order_by(InstanceObject.id_instance_object).all()
    instances = getobjectsjson(data, columns_instanceobject)
    
    data = Roi.query.filter(Roi.startyear>=400, Roi.startyear<=600).order_by(Roi.startyear).all()
    rois = getobjectsjson(data, columns_roi)

    data = Evenement.query.order_by(Evenement.startyear).filter(Evenement.startyear>400, Evenement.startyear<600).all()
    evenements = getobjectsjson(data, columns_evenement)

    data = Personnage.query.filter(Personnage.birthyear>=400, Personnage.birthyear<=600).order_by(Personnage.birthyear).all()
    personnages = getobjectsjson(data, columns_personnage)


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
    
    data = InstanceObject.query.order_by(InstanceObject.id_instance_object).all()
    instances = getobjectsjson(data, columns_instanceobject)
    return jsonify(instances)




############### LIEU ###############

@app.route('/lieu/edit', methods=['GET'])
def editlieu():
    data = Lieu.query.order_by(Lieu.id_lieu).all()
    lieux = getobjectsjson(data, columns_lieu)
    html = "<p>"+str(len(lieux))+"</p>"
    for row in lieux:
        form = "<form action='/lieu/form/update'>"
        form = form+"<input type='hidden' name='id_lieu' value=\""+str(row['id_lieu'])+"\"/>&nbsp;&nbsp;"
        form = form+"<textarea name='nom' rows='3' cols='50'>"+str(row['nom'])+"</textarea>&nbsp;&nbsp;"
        form = form+"<input size='5' name='lon' value=\""+str(row['lon'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='lat' value=\""+str(row['lat'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='inception' value=\""+str(row['inception'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='constructionyear' value=\""+str(row['constructionyear'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='prod' value=\""+str(row['prod'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input type='submit' name='button' value='Supprimer'>&nbsp;&nbsp;"
        form = form+"<input type='submit' name='button' value='Valider'></form>"
        html = html+form    
    return html

@app.route('/lieu/form/update', methods=['POST', 'GET'])
def updatelieu():
    body = request.values
    editData = Lieu.query.filter_by(id_lieu=body['id_lieu']).first()
    for key in body:
        if(body[key] == "None"):
            setattr(editData, key, None)
        else:
            setattr(editData, key, body[key])
    db.session.commit()
    return redirect("/lieu/edit", code=302)


@app.route('/lieu', methods=['POST', 'GET'])
def lieu():
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        data = Lieu(body['nom'],body['lon'],body['lat'],body['inception'],body['constructionyear'],body['prod'])
        db.session.add(data)
        db.session.commit()
        body['status'] = "All good"
        return jsonify(body)
    
    # GET all data from database & sort by id
    if request.method == 'GET':
        data = Lieu.query.order_by(Lieu.id_lieu).all()
        lieux = getobjectsjson(data, columns_lieu)
        return jsonify(lieux)


@app.route('/lieu/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onelieu(id):
    # GET a specific data by id
    if request.method == 'GET':
        return getonegeneric("lieu", columns_lieu, id)
        
    # DELETE a data
    if request.method == 'DELETE':
        return delonegeneric("lieu", id)

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        return putonegeneric("lieu", columns_lieu, id, body)




############ PERSONNAGE ##########


@app.route('/personnage/edit', methods=['GET'], defaults={'start': None, 'end': None})
@app.route('/personnage/edit/start/<start>/end/<end>', methods=['GET'])
def editpersonnage(start, end):
    if((start == None) & (end == None)):
        data = Personnage.query.order_by(Personnage.birthyear).all()
    else:
        data = Personnage.query.filter(Personnage.birthyear>=start, Personnage.birthyear<=end).order_by(Personnage.birthyear).all()

    personnages = getobjectsjson(data, columns_personnage)
    html = ""
    
    form = "<form action='/personnage/form/create'>"
    form = form+"<input size='20' name='nom' value=''/>&nbsp;&nbsp;"
    form = form+"<input size='10' name='dateofbirth' value=''/>&nbsp;&nbsp;"
    form = form+"<input size='10' name='placeofbirthlabel' value=''/>&nbsp;&nbsp;"
    form = form+"<input size='10' name='dateofdeath' value=''/>&nbsp;&nbsp;"
    form = form+"<input size='10' name='placeofdeathlabel' value=''/>&nbsp;&nbsp;"
    form = form+"<input size='10' name='positions' value=''/>&nbsp;&nbsp;"
    form = form+"<input size='5' name='birthyear' value=''/>&nbsp;&nbsp;"
    form = form+"<input size='5' name='deathyear' value=''/>&nbsp;&nbsp;"  
    form = form+"<input size='5' name='prod' value=''/>&nbsp;&nbsp;"  
    form = form+"<input type='submit' name='button' value='Ajouter'></form>"
    html = html+form
    
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
        form = form+"<input size='5' name='prod' value=\""+str(row['prod'])+"\"/>&nbsp;&nbsp;"  
        form = form+"<input type='submit' name='button' value='Valider'></form>"
        html = html+form 
    
    return html



@app.route('/personnage/form/create', methods=['POST','GET'])
def createpersonnage():
    body = request.values
    newbody = {}
    for key in body:
        if(body[key] == "None"):
            newbody[key] = None
        else:
            newbody[key] = body[key]
    data = Personnage(newbody['nom'],newbody['dateofbirth'],newbody['placeofbirthlabel'],newbody['dateofdeath'],newbody['placeofdeathlabel'],newbody['positions'],newbody['birthyear'],newbody['deathyear'],newbody['prod'])
    db.session.add(data)
    db.session.commit()
    return redirect("/personnage/edit", code=302)


@app.route('/personnage/form/update', methods=['POST', 'GET'])
def updatepersonnage():
    body = request.values
    editData = Personnage.query.filter_by(id_personnage=body['id_personnage']).first()
    for key in body:
        if(body[key] == "None"):
            setattr(editData, key, None)
        else:
            setattr(editData, key, body[key])
    db.session.commit()
    return redirect("/personnage/edit", code=302)


@app.route('/personnage', methods=['POST', 'GET'], defaults={'start': None, 'end': None})
@app.route('/personnage/start/<start>/end/<end>', methods=['POST', 'GET'])
def personnage(start, end):
    
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        data = Personnage(body['nom'],body['dateofbirth'],body['placeofbirthlabel'],body['dateofdeath'],body['placeofdeathlabel'],body['positions'],body['birthyear'],body['deathyear'],body['prod'])
        db.session.add(data)
        db.session.commit()
        body['status'] = "All good"
        return jsonify(body)

 
    # GET all data from database & sort by id
    if request.method == 'GET':
        if((start == None) & (end == None)):
            data = Personnage.query.order_by(Personnage.birthyear).all()
        else:
            data = Personnage.query.filter(Personnage.birthyear>=start, Personnage.birthyear<=end).order_by(Personnage.birthyear).all()
        personnages = getobjectsjson(data, columns_personnage)
        return jsonify(personnages)


@app.route('/personnage/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onepersonnage(id):
    # GET a specific data by id
    if request.method == 'GET':
        return getonegeneric("personnage", columns_personnage, id)
        
    # DELETE a data
    if request.method == 'DELETE':
        return delonegeneric("personnage", id)

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        return putonegeneric("personnage", columns_personnage, id, body)



############ ROI #############


@app.route('/roi/edit', methods=['GET'])
def editroi():
    year = None
    start = None
    end = None
    if(year == None):
        if((start == None) & (end == None)):
            data = Roi.query.order_by(Roi.startyear).all()
        else:
            data = Roi.query.filter(Roi.startyear>=start, Roi.startyear<=end).order_by(Roi.startyear).all()
    else:
        data = Roi.query.filter(Roi.startyear<=year, Roi.endyear>=year).order_by(Roi.startyear).all()

    rois = getobjectsjson(data, columns_roi)
    html = ""
    form = "<form action='/roi' method='post'>"
    form = form+"<input name='wikiid' value='' placeholder='wikiid' />&nbsp;&nbsp;"
    form = form+"<input size='10' name='nom' value='' placeholder='nom'/>&nbsp;&nbsp;"
    form = form+"<input size='10' name='dateofbirth' value='' placeholder='dateofbirth'/>&nbsp;&nbsp;"
    form = form+"<input size='10' name='placeofbirthlabel' value='' placeholder='placeofbirthlabel'/>&nbsp;&nbsp;"
    form = form+"<input size='10' name='dateofdeath' value='' placeholder='dateofdeath'/>&nbsp;&nbsp;"
    form = form+"<input size='10' name='placeofdeathlabel' value='' placeholder='placeofdeathlabel'/>&nbsp;&nbsp;"
    form = form+"<input type='hidden' size='5' name='mannersofdeath' value='' placeholder='mannersofdeath'/>&nbsp;&nbsp;"
    form = form+"<input size='5' name='placeofburiallabel' value='' placeholder='placeofburiallabel'/>&nbsp;&nbsp;"
    form = form+"<input type='hidden' size='5' name='fatherlabel' value='' placeholder='fatherlabel'/>&nbsp;&nbsp;"
    form = form+"<input type='hidden' size='5' name='motherlabel' value='' placeholder='motherlabel'/>&nbsp;&nbsp;"
    form = form+"<input type='hidden' size='5' name='spouses' value='' placeholder='spouses'/>&nbsp;&nbsp;"
    form = form+"<input size='10' name='starttime' value='' placeholder='starttime'/>&nbsp;&nbsp;"
    form = form+"<input size='10' name='endtime' value='' placeholder='endtime'/>&nbsp;&nbsp;"
    form = form+"<input size='5' name='startyear' value='' placeholder='startyear'/>&nbsp;&nbsp;"
    form = form+"<input size='5' name='endyear' value='' placeholder='endyear'/>&nbsp;&nbsp;"  
    form = form+"<input size='5' name='birthyear' value='' placeholder='birthyear'/>&nbsp;&nbsp;"
    form = form+"<input size='5' name='deathyear' value='' placeholder='deathyear'/>&nbsp;&nbsp;"  
    form = form+"<input size='1' name='prod' value='' placeholder='prod'/>&nbsp;&nbsp;"
    form = form+"<input name='urlimage' value='' placeholder='urlimage'/>&nbsp;&nbsp;"
    form = form+"<input type='submit' name='button' value='Supprimer'>&nbsp;&nbsp;"
    form = form+"<input type='submit' name='button' value='Valider'></form>"
    html = html+form 

    for row in rois:
        form = "<form action='/roi/form/update'>"
        form = form+"<input type='hidden' name='id_roi' value=\""+str(row['id_roi'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='wikiid' value=\""+str(row['wikiid'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='nom' value=\""+str(row['nom'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='dateofbirth' value=\""+str(row['dateofbirth'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='placeofbirthlabel' value=\""+str(row['placeofbirthlabel'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='dateofdeath' value=\""+str(row['dateofdeath'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='placeofdeathlabel' value=\""+str(row['placeofdeathlabel'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input type='hidden' size='5' name='mannersofdeath' value=\""+str(row['mannersofdeath'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input type='hidden' size='5' name='placeofburiallabel' value=\""+str(row['placeofburiallabel'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input type='hidden' size='5' name='fatherlabel' value=\""+str(row['fatherlabel'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input type='hidden' size='5' name='motherlabel' value=\""+str(row['motherlabel'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input type='hidden' size='5' name='spouses' value=\""+str(row['spouses'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='starttime' value=\""+str(row['starttime'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='endtime' value=\""+str(row['endtime'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='startyear' value=\""+str(row['startyear'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='endyear' value=\""+str(row['endyear'])+"\"/>&nbsp;&nbsp;"  
        form = form+"<input size='5' name='birthyear' value=\""+str(row['birthyear'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='deathyear' value=\""+str(row['deathyear'])+"\"/>&nbsp;&nbsp;"  
        form = form+"<input size='1' name='prod' value=\""+str(row['prod'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='urlimage' value=\""+str(row['urlimage'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input type='submit' name='button' value='Supprimer'>&nbsp;&nbsp;"
        form = form+"<input type='submit' name='button' value='Valider'></form>"
        html = html+form 
    return html

@app.route('/roi/form/update', methods=['POST', 'GET'])
def updateroi():
    body = request.values
    editData = Roi.query.filter_by(id_roi=body['id_roi']).first()
    for key in body:
        print(key)
        if(body[key] == "None"):
            setattr(editData, key, None)
        else:
            setattr(editData, key, body[key])
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
        if(request.json == None):
            body = request.form
        else:
            body = request.json
        newbody = {}
        for key in body:
            if((body[key] == "None") | (body[key] == "")):
                newbody[key] = None
            else:
                newbody[key] = body[key]
        print(newbody)

        data = Roi(newbody['wikiid'],newbody['nom'],newbody['dateofbirth'],newbody['placeofbirthlabel'],newbody['dateofdeath'],newbody['placeofdeathlabel'],newbody['mannersofdeath'],newbody['placeofburiallabel'],newbody['fatherlabel'],newbody['motherlabel'],newbody['spouses'],newbody['starttime'],newbody['endtime'],newbody['startyear'],newbody['endyear'],newbody['birthyear'],newbody['deathyear'],newbody['urlimage'],newbody['prod'])
        db.session.add(data)
        db.session.commit()
        newbody['status'] = "All good"
        return jsonify(newbody)
    
    # GET all data from database & sort by id
    if request.method == 'GET':
        if(year == None):
            if((start == None) & (end == None)):
                data = Roi.query.order_by(Roi.startyear).all()
            else:
                data = Roi.query.filter(Roi.startyear>=start, Roi.startyear<=end).order_by(Roi.startyear).all()
        else:
            data = Roi.query.filter(Roi.startyear<=year, Roi.endyear>=year).order_by(Roi.startyear).all()

        rois = getobjectsjson(data, columns_roi)
        return jsonify(rois)

@app.route('/roi/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def oneroi(id):
     # GET a specific data by id
    if request.method == 'GET':
        return getonegeneric("roi", columns_roi, id)
        
    # DELETE a data
    if request.method == 'DELETE':
        return delonegeneric("roi", id)

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        return putonegeneric("roi", columns_roi, id, body)


############## EVENEMENT ################

@app.route('/evenement/edit', methods=['GET'], defaults={'start': None, 'end': None})
@app.route('/evenement/edit/start/<start>/end/<end>', methods=['GET'])
def editevenement(start, end):
    if((start == None) & (end == None)):
        data = Evenement.query.order_by(Evenement.id_event).all()
    else:
        data = Evenement.query.order_by(Evenement.startyear).filter(Evenement.startyear>start, Evenement.startyear<end).all()
    evenements = getobjectsjson(data, columns_evenement)

    html = "<p>"+str(len(evenements))+"</p>"
    for row in evenements:
        form = "<form action='/evenement/form/update'>"
        form = form+"<input name='id_event' value=\""+str(row['id_event'])+"\"/>&nbsp;&nbsp;"
        form = form+"<textarea name='evenement' rows='3' cols='50'>"+str(row['evenement'])+"</textarea>&nbsp;&nbsp;"
        form = form+"<input size='5' name='startyear' value=\""+str(row['startyear'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='endyear' value=\""+str(row['endyear'])+"\"/>&nbsp;&nbsp;"
        form = form+"<textarea name='commentaire' rows='3' cols='50'>"+str(row['commentaire'])+"</textarea>&nbsp;&nbsp;"
        form = form+"<textarea name='prod' rows='3' cols='50'>"+str(row['prod'])+"</textarea>&nbsp;&nbsp;"
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
        data = Evenement(body['evenement'], body['startyear'], body['endyear'], body['commentaire'],body['prod'])
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
        evenements = getobjectsjson(data, columns_evenement)
        return jsonify(evenements)

@app.route('/evenement/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def oneevenement(id):
    columns = ['id_event','evenement','startyear','endyear','commentaire']

    # GET a specific data by id
    if request.method == 'GET':
        return getonegeneric("evenement", columns_evenement, id)
        
    # DELETE a data
    if request.method == 'DELETE':
        return delonegeneric("evenement", id)

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        return putonegeneric("evenement", columns_evenement, id, body)


####### GENERIC FUNCTIONS #######

def getonedata(type, id):
    if(type == "evenement"): 
        data = Evenement.query.get(id)
    if(type == "roi"): 
        data = Roi.query.get(id)
    if(type == "lieu"): 
        data = Lieu.query.get(id)
    if(type == "personnage"): 
        data = Personnage.query.get(id)
    if(type == "user"):
        data = UserInfo.query.get(id)

    return data

def getonegeneric(type, columns, id):
    data = getonedata(type, id)
    dataDict = {}
    j = 0
    for key in columns:
        dataDict[key] = str(data).split('/')[j]
        j = j + 1
    return jsonify(dataDict)

def delonegeneric(type, id):
    delData = getonedata(type, id)
    db.session.delete(delData)
    db.session.commit()
    return jsonify({'status': 'Data '+id+' is deleted from PostgreSQL!'})

def putonegeneric(type, columns, id, body):
    editData = getonedata(type, id)
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
            print("key " + key + " value " + str(data[i]).split('/')[j])
            dataDict[key] = str(data[i]).split('/')[j]
            j = j + 1
        dataJson.append(dataDict)
    return dataJson


def genlat():
    rand = random.random()
    lat = (48.903767 - 48.811945)*rand+48.811945
    return "%.6f" %lat

def genlon():
    rand = random.random()
    lon = (2.416740 - 2.251700)*rand+2.251700
    return "%.6f" %lon


if __name__ == '__main__':
    app.debug = True
    app.run()
