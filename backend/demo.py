from flask import Flask, request, render_template,redirect
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



@app.route('/api/evenement/year/<year>')
def list_evts(year):
    sql_query = """SELECT * FROM evenement WHERE startYear <= """+year+""" and endYear >= """+year
    evts = pd.read_sql(sql_query, engine)
    return evts.to_json(orient='records')



@app.route('/list/evenement/', defaults={'startperiod': None, 'endperiod': None, 'updated':0})
@app.route('/list/evenement/updated/<updated>', defaults={'startperiod': None, 'endperiod': None})
@app.route('/list/evenement/startperiod/<startperiod>/endperiod/<endperiod>', defaults={'updated':0})
@app.route('/list/evenement/startperiod/<startperiod>/endperiod/<endperiod>/updated/<updated>')
def update_evts(startperiod, endperiod, updated):
    if((startperiod == None) & (endperiod == None)):
        sql_query = """SELECT * FROM evenement"""
    else:
        sql_query = """SELECT * FROM evenement WHERE startYear >= """+startperiod+""" and startYear <= """+endperiod
    evts = pd.read_sql(sql_query, engine)
    if(updated == 0):
        html = ""
    else:
        html = "<p>Changement pris en compte !</p><br />"

    for index, row in evts.iterrows():
        form = "<form action='/update/evenement'>"
        if(startperiod != None):
            form = form+"<input type='hidden' name='startperiod' value='"+startperiod+"'/>&nbsp;&nbsp;"
        if(endperiod != None):
            form = form+"<input type='hidden' name='endperiod' value='"+endperiod+"'/>&nbsp;&nbsp;"
        form = form+"<input type='hidden' name='id_event' value='"+str(row['id_event'])+"'/>&nbsp;&nbsp;"
        form = form+"<textarea name='evenement' rows='3' cols='50'>"+str(row['evenement'])+"</textarea>&nbsp;&nbsp;"
        form = form+"<input size='5' name='startyear' value='"+str(row['startyear'])+"'/>&nbsp;&nbsp;"
        form = form+"<input size='5' name='endyear' value='"+str(row['endyear'])+"'/>&nbsp;&nbsp;"
        form = form+"<textarea name='commentaire' rows='3' cols='50'>"+str(row['commentaire'])+"</textarea>&nbsp;&nbsp;"
        form = form+"<input type='submit' name='button' value='Supprimer'>&nbsp;&nbsp;"
        form = form+"<input type='submit' name='button' value='Valider'></form>"
        html = html+form

    html = html+"<p>Nouvel Evenement :</p>"
    form = "<form action='/create/evenement'>"
    if(startperiod != None):
            form = form+"<input type='hidden' name='startperiod' value='"+startperiod+"'/>&nbsp;&nbsp;"
    if(endperiod != None):
        form = form+"<input type='hidden' name='endperiod' value='"+endperiod+"'/>&nbsp;&nbsp;"
    form = form+"<textarea name='evenement' rows='3' cols='50'></textarea>&nbsp;&nbsp;"
    form = form+"<input size='5' name='startyear' value=''/>&nbsp;&nbsp;"
    form = form+"<input size='5' name='endyear' value=''/>&nbsp;&nbsp;"
    form = form+"<textarea name='commentaire' rows='3' cols='50'></textarea>&nbsp;&nbsp;"
    form = form+"<input type='submit' value='Submit'></form>"
    html = html + form
    return html



@app.route('/create/evenement')
def create_evenement():
    if(request.values.get('startperiod') != None):
        startperiod = request.values['startperiod']
    else:
        startperiod = None
    if(request.values.get('endperiod') != None):
        endperiod = request.values['endperiod']
    else:
        endperiod = None
    evenement = request.values['evenement']
    startyear = request.values['startyear']
    endyear = request.values['endyear']
    commentaire = request.values['commentaire']

    sql_query = """INSERT INTO evenement(evenement,startyear,endyear,commentaire) VALUES ('"""+evenement+"""', """+startyear+""", """+endyear+""", '"""+commentaire+"""')""" 
    engine.execute(sql_query)
    if((startperiod == None) & (endperiod == None)):
        return redirect("/list/evenement/updated/1", code=302)
    else:
        return redirect("/list/evenement/startperiod/"+startperiod+"/endperiod/"+endperiod+"/updated/1", code=302)


@app.route('/update/evenement')
def update_evenement():
    if(request.values.get('startperiod') != None):
        startperiod = request.values['startperiod']
    else:
        startperiod = None
    if(request.values.get('endperiod') != None):
        endperiod = request.values['endperiod']
    else:
        endperiod = None
    id_event = request.values['id_event']
    evenement = request.values['evenement']
    startyear = request.values['startyear']
    endyear = request.values['endyear']
    commentaire = request.values['commentaire']
    
    if(request.values['button'] == "Valider"):
        sql_query = """UPDATE evenement SET evenement = '"""+evenement+"""', startyear = """+startyear+""", endyear = """+endyear+""", commentaire = '"""+commentaire+"""'  WHERE id_event = """+id_event
    else:
        sql_query = """DELETE FROM evenement WHERE id_event = """+id_event

    engine.execute(sql_query)
    if((startperiod == None) & (endperiod == None)):
        return redirect("/list/evenement/updated/1", code=302)
    else:
        return redirect("/list/evenement/startperiod/"+startperiod+"/endperiod/"+endperiod+"/updated/1", code=302)



def html_input(c):
    return '<input name="{}" value="{{}}" />'.format(c)


if __name__ == "__main__":
    app.run(debug=True)