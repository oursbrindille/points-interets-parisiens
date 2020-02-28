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


class InstanceRoi(db.Model):
    __tablename__ = "instance_roi"
    id_instance_roi = db.Column(db.Integer, primary_key=True)
    id_roi = db.Column(db.Integer)
    lon = db.Column(db.Float)
    lat = db.Column(db.Float)

    def __init__(self, id_roi, lon, lat):
        self.id_roi = id_roi
        self.lon = lon
        self.lat = lat
    
    def __repr__(self):
        return '%s/%s/%s/%s' % (self.id_instance_roi, self.id_roi, self.lon, self.lat)


def genlat():
    rand = random.random()
    lat = (48.903767 - 48.811945)*rand+48.811945
    return "%.6f" %lat

def genlon():
    rand = random.random()
    lon = (2.416740 - 2.251700)*rand+2.251700
    return "%.6f" %lon

@app.route('/generate')
def generate():
    instances = getinstanceroijson()
    html = ""
    for instance in instances:
        delData = InstanceRoi.query.filter_by(id_instance_roi=instance["id_instance_roi"]).first()
        db.session.delete(delData)
        db.session.commit()

    for i in range(10):
        data = InstanceRoi("12", genlon(), genlat())
        db.session.add(data)
        db.session.commit()
    
    instances = getinstanceroijson()
    return jsonify(instances)

@app.route('/instance-roi', methods=['POST', 'GET'])
def instanceroi():
    
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
        instances = getinstanceroijson()
        return jsonify(instances)

def getinstanceroijson():
    # data = User.query.all()
    data = InstanceRoi.query.order_by(InstanceRoi.id_instance_roi).all()
    print(data)
    dataJson = []
    for i in range(len(data)):
        # print(str(data[i]).split('/'))
        dataDict = {
            'id_instance_roi': str(data[i]).split('/')[0],
            'id_roi': str(data[i]).split('/')[1],
            'lon': str(data[i]).split('/')[2],
            'lat': str(data[i]).split('/')[3]
        }
        dataJson.append(dataDict)
    return dataJson


if __name__ == '__main__':
    app.debug = True
    app.run(port=5001)