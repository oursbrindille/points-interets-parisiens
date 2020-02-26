from flask import Flask, request, render_template,redirect
import pandas as pd
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

CORS(app)

config = pd.read_csv('config.csv', header=None)
id = config[0][0]
pwd = config[0][1]
host = config[0][2]
db = config[0][3]
#engine = create_engine('postgresql://%s:%s@%s/%s'%(id, pwd, host, db), client_encoding='utf8')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%s:%s@%s/%s'%(id, pwd, host, db)

db = SQLAlchemy(app)

from models import Evenement


@app.route('/')
def index():
    return "BackEnd King"


if __name__ == "__main__":
    app.run(debug=True)