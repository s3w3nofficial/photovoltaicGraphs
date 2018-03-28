from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import pandas as pd
import tempfile
import shutil
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

def fetchlocaldata(urlTmpl, format, datestart, dateend):
    # Returns directory name with fetched local data. Caller is responsible for its deletion.
    date = datestart
    delta = timedelta(days=1)
    basepath = tempfile.mkdtemp()
    while date < dateend:
        filename = date.strftime(format)
        url = '%s/%s' % (urlTmpl, filename)
        r = requests.get(url, stream=True)
        local_filepath = os.path.join(basepath, filename)
        with open(local_filepath, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        date += delta
    return basepath

@app.route('/graph', methods=['POST', 'GET'])
def showGraph():
    return render_template("graph.html")

if __name__ == "__main__":
    app.run(debug=True)
