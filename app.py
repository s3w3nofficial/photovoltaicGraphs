from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta, date
import pandas as pd
import tempfile
import shutil
import requests
import os

app = Flask(__name__)
requests.utils.default_user_agent = lambda: "Kyberna school project, https://kyberna.cz, urbanec.martin@ssakhk.cz"

@app.route('/')
def index():
    return render_template("index.html")

def fetchlocaldata(basepath='/tmp', urlTmpl='http://is.ssakhk.cz/graf', format='%Y_%m_%d.txt', datestart=date(2012, 1, 1), dateend=date(2013, 1, 1)):
    # Fills directory with data from local server
    date = datestart
    delta = timedelta(days=1)
    #basepath = tempfile.mkdtemp()
    while date < dateend:
        filename = date.strftime(format)
        url = '%s/%s' % (urlTmpl, filename)
        r = requests.get(url, stream=True)
        local_filepath = os.path.join(basepath, filename)
        with open(local_filepath, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        date += delta
    return basepath

def fetchremotedata(basepath='/tmp', raddatabase="PVGIS-CMASF", lat=50, lon=15, mountingplace="free", angle=0, azimuth=0, startyear=2007, endyear=2016, pvtech="crystSi", peakpower=0, loss=0):
    url = 'http://re.jrc.ec.europa.eu/pvgis5/seriescalc.php'
    payload = {
        'lat': lat,
        'lon': lon,
        'mountingplace': mountingplace,
        'hourlyangle': angle,
        'hourlyaspect': azimuth,
        'startyear': startyear,
        'endyear': endyear,
        'pvtechchoice': pvtech,
        'peakpower': peakpower,
        'loss': loss,
    }
    r = requests.get(url, params=payload)
    with open(os.path.join(basepath, 'remotedata.csv'), 'wb') as f:
        f.write(r.content)
    return os.path.join(basepath, 'remotedata.csv')


def readCSV(PATH):
    data = pd.read_csv(PATH, usecols=[0, 1], skiprows=10, skipfooter=10, engine='python', skip_blank_lines=True)

@app.route('/graph')
def showGraph():
    return render_template("graph.html")

if __name__ == "__main__":
    app.run(debug=True)
