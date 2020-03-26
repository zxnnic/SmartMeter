from flask import Flask, render_template
from graph import GraphRT, GraphS
from database import Database
import sys, atexit

from db_settings_secret import *

# create flask app
app = Flask(__name__)

# set up database
db = Database(DB_USERNAME,
                DB_PASSWORD,
                '127.0.0.1', 
                '3306',
                'smart_meter_db')
db.setup()

# set up route to template
@app.route("/")
def home():
    return render_template("home.html")
@app.route("/graph/realtime")
def realtime():
    graph = GraphRT(db,time_interval=2)
    atexit.register(graph.shutdown)
    return render_template("graph_rt.html")
@app.route("/graph/preloaded")
def preloaded():
    # time_interval is minute between each point
    graph = GraphS(db, time_interval=15, num_pts = 500)
    atexit.register(graph.shutdown)
    data = graph.graphIt()
    return render_template("graph_s.html",consumed=data['consumption'],generated=data['generation'])

# run the Flask app
app.run(debug=True, use_reloader=False)