import os
from flask import Flask, render_template, request, send_from_directory
import fetch
import dirwalk
import pandas as pd

app = Flask(__name__)

resultlist = []
query = " "


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/')
def main():
    return render_template('index.html',showslist=dirwalk.showslist())


# favicon route
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        global query
        global resultlist
        query = request.form['query']
        if query not in dirwalk.showslist():
            resultlist = fetch.main(query)
        else:
            df = pd.read_csv('data/' + query + '.csv')
            resultlist.append(len(df))
            df["polarity"] = pd.to_numeric(df["polarity"], errors='coerce')
            df["subjectivity"] = pd.to_numeric(df["subjectivity"], errors='coerce')
            resultlist.append(df["polarity"].mean())
            resultlist.append(df['subjectivity'].mean())
            if float(resultlist[1]) > 0:
                resultlist.append('Positive')
            elif float(resultlist[1]) == 0:
                resultlist.append('Neutral')
            else:
                resultlist.append('Negative')
    return render_template("result.html", query=query, tweets_count=resultlist[0], avgpol=resultlist[1],
                           avgsub=resultlist[2], pol=resultlist[3])


@app.route('/list')
def list():
    showlist = dirwalk.showslist()
    return render_template("list.html", showlist=showlist)


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True)
