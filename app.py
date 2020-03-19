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
    if static:
        # time_interval is minute between each point
        graph = GraphS(db, time_interval=15, num_pts = 500)
        atexit.register(graph.shutdown)    
        return render_template("graph_s.html",graph=graph.graphIt())
    else:
        # time_interval is seconds between each point
        graph = GraphRT(db,time_interval=10)
        atexit.register(graph.shutdown)
        return render_template("graph_rt.html")

# For determining realtime or not
def isStatic(argv):
    try:  
        if len(argv)>1:
            assert argv[1] == '-realtime', 'You have entered an invalid argument. The valid options are:\npython app.py\t\t\tFor static graphs\npython app.py -realtime\t\tFor realtime live graphs'
            static = False
        else:
            static = True
    except Exception as error:
        for err in error.args:
            print(err)
        print('\nThe app will be exiting. See yall later bye :^)')
    else:
        return static

static = isStatic(sys.argv)

# run the Flask app
app.run(debug=True, use_reloader=static)