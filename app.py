from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/graph', methods=['POST'])
def showGraph(data):
    return jsonify({"success":"true"})

if __name__ == "__main__":
    app.run(debug=True)
