from flask import Flask, request, render_template
import pandas as pd
from flask_cors import CORS
from sqlalchemy import create_engine
import os


app = Flask(__name__)

CORS(app)

@app.route('/list')
def list():
    path = "/home/geof/projects/monuments-paris/csv"
    string = "<ul>"

    for filename in os.listdir(path):
        string = string+"<li>"+filename+"</li>"
    string = string+"</ul>"
    return string+"<br /><form action='/edit'><input type='text' name='csvfile'><input type='submit' value='Submit'></form>"


@app.route('/edit')
def edit():
    csvfile = request.values['csvfile']
    df = pd.read_csv("../csv/"+csvfile)
    html = df.style.format({c: html_input(c) for c in df.columns}).render()
    return "<form action='/results'>"+html+"<input type='submit' value='Submit'></form>"


@app.route('/results')
def results():
    dfr = pd.DataFrame(request.values.lists())
    new_df = dfr
    dicto = {}
    for index, row in dfr.iterrows():
        dicto.update( {row[0] : row[1]})
    
    new_df = pd.DataFrame(dicto)

    new_df.to_csv("./test.csv", index=False)
    return new_df.to_json(orient='records')
    

def html_input(c):
    return '<input name="{}" value="{{}}" />'.format(c)


if __name__ == "__main__":
    app.run(debug=True)