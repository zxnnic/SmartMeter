import requests, json, time, plotly
import plotly.graph_objs as go
import mysql.connector
from pusher import Pusher
from database import Database
from mysql.connector import Error
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

class GraphRT:
    def __init__(self,db,time_interval):
        self.db = db
        self.scheduler = self.setup_scheduler(time_interval)
        self.pusher = self.setup_pusher()
        self.time = []
        self.energy = {'consumption':[], 'generation':[]}

    def setup_scheduler(self,time_interval):
        '''
        Create schedule for retrieving prices
        Returns: scheduler object
        '''
        scheduler = BackgroundScheduler()
        scheduler.start()
        scheduler.add_job(
            func=self.graphIt,
            trigger=IntervalTrigger(seconds=time_interval),
            id='get_energy',
            name='Retrieve energy information every 30 seconds',
            replace_existing=True)
        
        return scheduler

    def setup_pusher(self):
        ''' 
        Configure pusher object
        '''
        pusher = Pusher(
            app_id='969963',
            key='3f01e1d36db05ef9e19b',
            secret='1042ca3ae4c69ed45061',
            cluster='us3',
            ssl=True
        )
        return pusher

    def getData(self):
        data = self.db.getQuery('''
                                SELECT *
                                FROM e_sim
                                ORDER BY tstamp DESC
                                LIMIT 1;
                                ''')
        return data[0]

    def unixToDatetime(self,unix_time):
        return datetime.fromtimestamp(int(unix_time))

    def graphIt(self):
        data = self.getData()
        # add data to the appropriate channel
        self.time.append(self.unixToDatetime(data[0]))
        self.energy['consumption'].append(round(float(data[1])+float(data[2])))
        self.energy['generation'].append(round(float(data[2])))
        
        # put the data into axis for Plotly
        c_data = [go.Scatter(
            x=self.time,
            y=self.energy['consumption'],
            name="Consumed Energy",
            line={'color':'#A6C55B'}
        )]
        g_data = [go.Scatter(
            x=self.time,
            y=self.energy['generation'],
            name="Generated Energy",
            line={'color':'#A6C55B'}
        )]
        data = {
            'consumption': json.dumps(c_data, cls=plotly.utils.PlotlyJSONEncoder),
            'generation': json.dumps(g_data, cls=plotly.utils.PlotlyJSONEncoder)
        }
        # trigger event
        self.pusher.trigger("smartmeter", "data-updated", data)
    
    def shutdown(self):
        self.scheduler.shutdown()
        self.db.close()

class GraphS:
    def __init__(self, db, time_interval, num_pts):
        assert isinstance(time_interval,int), "Time interval entered is not an integer"
        assert isinstance(num_pts, int), "Number of points specified is not an integer"
        assert time_interval > 0, "Invalid time interval given"
        assert num_pts > 0, "Invalid number of points given"
        self.db = db
        self.time_interval = time_interval
        self.num_pts = num_pts
        self.time = []
        self.energy = {'consumption':[], 'generation':[]}

    def getData(self):
        '''
        Get the amount of rows specified by num_pts from the database
        '''
        limit=self.num_pts*self.time_interval
        query = self.db.getQuery('''
                                    SELECT p.tstamp, p.grid, p.solarp
                                    FROM (
                                        SELECT @row := @row +1 AS rownum, tstamp, grid, solarp
                                        FROM (SELECT @row :=0) r, profiles
                                        LIMIT {0}
                                    ) p
                                    WHERE p.rownum % {1} = 0
                                '''.format(limit,self.time_interval))
        return query

    def unixToDatetime(self,unix_time):
        return datetime.fromtimestamp(int(unix_time))

    def graphIt(self):
        data = self.getData()
        for t,g,s in data:
            self.time.append(self.unixToDatetime(t))
            self.energy['consumption'].append(round(float(g)+float(s)))
            self.energy['generation'].append(round(float(s)))
        
        # put the data into axis for Plotly
        c_data = [go.Scatter(
            x=self.time,
            y=self.energy['consumption'],
            name="Consumed Energy",
            line={'color':'#A6C55B'}
        )]
        g_data = [go.Scatter(
            x=self.time,
            y=self.energy['generation'],
            name="Generated Energy",
            line={'color':'#A6C55B'}
        )]
        data = {
            'consumption': json.dumps(c_data, cls=plotly.utils.PlotlyJSONEncoder),
            'generation': json.dumps(g_data, cls=plotly.utils.PlotlyJSONEncoder)
        }
        return data

    def shutdown(self):
        self.db.close()

### For testing ###
from db_settings_secret import *
if __name__ == "__main__":
    # set up database
    db = Database(DB_USERNAME,
                    DB_PASSWORD,
                    '127.0.0.1', 
                    '3306',
                    'smart_meter_db')
    db.setup() 
    graph = GraphS(db,15,2)
    print(graph.graphIt())