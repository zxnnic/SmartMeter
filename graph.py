import requests, json, time, plotly
import plotly.graph_objs as go
from pusher import Pusher
from database import Database

from db_settings_secret import *

def setup_pusher():
    ''' 
    Configure pusher object
    '''
    pusher = Pusher(
        app_id='962040',
        key='fab32afad87f9a9d80a6',
        secret='4e3291c27abf38f7c9eb',
        cluster='us3',
        ssl=True
    )
    return pusher

def graph():
    # set up pusher object
    pusher = setup_pusher()
    # set up database
    db = Database(DB_USERNAME,
                    DB_PASSWORD,
                    '127.0.0.1', 
                    '3306',
                    'smart_meter_db')
    db.setup() 
    # set up time and energy produced/consumed dictionary
    time = []
    energy = {'solar_prod':[], 'load_cons':[]}
    # get info from database
    
    # append info to a list for graph

    # create a line graph

    # dump the data into json for transfering to front end

    # create trigger event