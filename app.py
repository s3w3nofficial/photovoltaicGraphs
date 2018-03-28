from flask import Flask, render_template, jsonify
from datetime import datetime
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

def downloadlocaldata(url, datestart, dateend):
    pass

@app.route('/graph', methods=['POST', 'GET'])
def showGraph():
    return render_template("graph.html")

if __name__ == "__main__":
    app.run(debug=True)
