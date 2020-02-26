from flask import Flask, render_template, request, jsonify
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

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/data', methods=['POST', 'GET'])
def data():
    
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
        return jsonify(dataJson)

@app.route('/data/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):

    # GET a specific data by id
    if request.method == 'GET':
        data = Evenement.query.get(id)
        print(data)
        dataDict = {
            'id_event': str(data[i]).split('/')[0],
            'evenement': str(data[i]).split('/')[1],
            'startyear': str(data[i]).split('/')[2],
            'endyear': str(data[i]).split('/')[3],
            'commentaire': str(data[i]).split('/')[4]
        }
        return jsonify(dataDict)
        
    # DELETE a data
    if request.method == 'DELETE':
        delData = Evenement.query.filter_by(id=id).first()
        db.session.delete(delData)
        db.session.commit()
        return jsonify({'status': 'Data '+id+' is deleted from PostgreSQL!'})

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        editData = Evenement.query.filter_by(id=id).first()
        editData.evenement = body['evenement']
        editData.startyear = body['startyear']
        editData.endyear = body['endyear']
        editData.commentaire = body['commentaire']
        db.session.commit()
        return jsonify({'status': 'Data '+id+' is updated from PostgreSQL!'})

if __name__ == '__main__':
    app.debug = True
    app.run()
