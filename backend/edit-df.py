from flask import Flask, request, render_template
import pandas as pd
from flask_cors import CORS
from sqlalchemy import create_engine

df = pd.read_csv("../csv/rois-france-avec-dates.csv")

app = Flask(__name__)

CORS(app)

@app.route('/')
def index():
    html = df.style.format({c: html_input(c) for c in df.columns}).render()
    return "<form action='/toto'>"+html+"<input type='submit' value='Submit'></form>"

@app.route('/results')
def toto():
    dfr = pd.DataFrame(request.values.lists())
    #dfr = dfr.transpose()
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