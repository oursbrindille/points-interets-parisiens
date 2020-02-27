from flask import Flask, render_template, request, jsonify,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import yaml

app = Flask(__name__)
db_config = yaml.load(open('database.yaml'))
app.config['SQLALCHEMY_DATABASE_URI'] = db_config['uri']
db = SQLAlchemy(app)
CORS(app)

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
    
    def __repr__(self):
        return '%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s' % (self.id_roi,self.wikiid,self.nom,self.dateofbirth,self.placeofbirthlabel,self.dateofdeath,self.placeofdeathlabel,self.mannersofdeath,self.placeofburiallabel,self.fatherlabel,self.motherlabel,self.spouses,self.starttime,self.endtime,self.startyear,self.endyear)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/roi/edit', methods=['GET'])
def editroi():
    rois = getroijson()
    html = ""
    for row in rois:
        form = "<form action='/roi/form/update'>"
        form = form+"<input type='hidden' name='id_roi' value=\""+str(row['id_roi'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input type='hidden' name='wikiid' value=\""+str(row['wikiid'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='20' name='nom' value=\""+str(row['nom'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='dateofbirth' value=\""+str(row['dateofbirth'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='placeofbirthlabel' value=\""+str(row['placeofbirthlabel'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='dateofdeath' value=\""+str(row['dateofdeath'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='placeofdeathlabel' value=\""+str(row['placeofdeathlabel'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='mannersofdeath' value=\""+str(row['mannersofdeath'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='placeofburiallabel' value=\""+str(row['placeofburiallabel'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='fatherlabel' value=\""+str(row['fatherlabel'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='motherlabel' value=\""+str(row['motherlabel'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='spouses' value=\""+str(row['spouses'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='starttime' value=\""+str(row['starttime'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='10' name='endtime' value=\""+str(row['endtime'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='startyear' value=\""+str(row['startyear'])+"\"/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='endyear' value=\""+str(row['endyear'])+"\"/>&nbsp;&nbsp;"  
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
    
    db.session.commit()
    return redirect("/roi/edit", code=302)


@app.route('/roi', methods=['POST', 'GET'])
def roi():
    
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

        data = Roi(wikiid,nom,dateofbirth,placeofbirthlabel,dateofdeath,placeofdeathlabel,mannersofdeath,placeofburiallabel,fatherlabel,motherlabel,spouses,starttime,endtime,startyear,endyear)
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
            'endyear': endyear

        })
    
    # GET all data from database & sort by id
    if request.method == 'GET':
        rois = getroijson()
        return jsonify(rois)

def getroijson():
    # data = User.query.all()
    data = Roi.query.order_by(Roi.startyear).all()
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
            'endyear': str(data[i]).split('/')[15]
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
            'endyear': str(data).split('/')[15]
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

        db.session.commit()
        return jsonify({'status': 'Data '+id+' is updated from PostgreSQL!'})


@app.route('/evenement/edit', methods=['GET'])
def editevenement():
    evenements = getevenementjson()
    html = ""
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


@app.route('/evenement', methods=['POST', 'GET'])
def evenement():
    
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
        evenements = getevenementjson()
        return jsonify(evenements)

def getevenementjson():
    # data = User.query.all()
    data = Evenement.query.order_by(Evenement.id_event).all()
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
