from flask import Flask, request, render_template
import pandas as pd


df_kings = pd.read_csv("../rois-france-avec-dates.csv")

app = Flask(__name__)

@app.route('/')
def index():
    df_king = which_king(1543)
    #return df_king.to_html()
    return render_template('myform.html')


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']    
    df_king = which_king(int(text))
    return df_king.to_html()

def which_king(year):
    df_king = df_kings[df_kings["startYear"] <= year]
    df_king = df_king[df_king["endYear"] > year]
    return df_king

if __name__ == "__main__":
    app.run(debug=True)