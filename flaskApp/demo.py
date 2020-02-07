from flask import Flask, request, render_template
import pandas as pd
from flask_cors import CORS


df_kings = pd.read_csv("../rois-france-avec-dates.csv")
df_monuments = pd.read_csv("../monuments-paris-avec-dates.csv")

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "BackEnd King"


@app.route('/king/year/<year>')
def king_date(year):
    df_king = which_king(int(year))
    return df_king.to_json(orient='records')


@app.route('/monument/year/<year>')
def monument_date(year):
    df_monument = which_monument(int(year))
    return df_monument.to_json(orient='records')


def which_king(year):
    df_king = df_kings[df_kings["startYear"] <= year]
    df_king = df_king[df_king["endYear"] > year]
    return df_king
    
def which_monument(year):
    df_monument = df_monuments[df_monuments["constructionYear"] <= year]
    return df_monument

if __name__ == "__main__":
    app.run(debug=True)