from flask import Flask, request, render_template
import pandas as pd
from flask_cors import CORS
from sqlalchemy import create_engine

df_kings = pd.read_csv("../csv/rois-france-avec-dates.csv")
df_monuments = pd.read_csv("../csv/monuments-paris-avec-dates.csv")
df_evts = pd.read_csv("../csv/concat/evenements-paris.csv")
df_persos = pd.read_csv("../csv/parismoyenage/extract-persos-paris-clean.csv")

app = Flask(__name__)

CORS(app)


config = pd.read_csv('config.csv', header=None)
id = config[0][0]
pwd = config[0][1]
host = config[0][2]
db = config[0][3]
engine = create_engine('postgresql://%s:%s@%s/%s'%(id, pwd, host, db), client_encoding='utf8')


@app.route('/')
def index():
    return "BackEnd King"


@app.route('/test/king/year/<year>')
def king_date(year):
    df_king = which_king(int(year))
    return df_king.to_json(orient='records')


@app.route('/test/monument/year/<year>')
def monument_date(year):
    df_monument = which_monument(int(year))
    return df_monument.to_json(orient='records')


@app.route('/test/evenement/year/<year>')
def evenement_date(year):
    df_evt = which_evenement(int(year))
    return df_evt.to_json(orient='records')


@app.route('/api/evenement/year/<year>')
def list_evts(year):
    sql_query = """SELECT * FROM evenement WHERE startYear <= """+year+""" and endYear >= """+year
    evts = pd.read_sql(sql_query, engine)
    return evts.to_json(orient='records')


@app.route('/test/personnage/year/<year>')
def perso_date(year):
    df_perso = which_perso(int(year))
    return df_perso.to_json(orient='records')


def which_king(year):
    df_king = df_kings[df_kings["startYear"] <= year]
    df_king = df_king[df_king["endYear"] >= year]
    return df_king
    
def which_monument(year):
    df_monument = df_monuments[df_monuments["constructionYear"] <= year]
    return df_monument

    
def which_evenement(year):
    df_evt = df_evts[df_evts["startYear"] <= year]
    df_evt = df_evt[df_evts["endYear"] >= year]
    return df_evt

    
def which_perso(year):
    df_perso = df_persos[df_persos["birthYear"] <= year]
    df_perso = df_perso[df_perso["deathYear"] >= year]
    return df_perso

if __name__ == "__main__":
    app.run(debug=True)