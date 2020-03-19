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
        self.time_interval = time_interval
        self.scheduler = self.setup_scheduler()
        self.pusher = self.setup_pusher()
        self.time = []
        self.energy = {'solar_prod':[], 'grid_cons':[]}

    def setup_scheduler(self):
        '''
        Create schedule for retrieving prices
        Returns: scheduler object
        '''
        scheduler = BackgroundScheduler()
        scheduler.start()
        scheduler.add_job(
            func=self.graphIt,
            trigger=IntervalTrigger(seconds=self.time_interval),
            id='get_energy',
            name='Retrieve solar energy produced every 10 seconds',
            replace_existing=True)
        
        return scheduler

    def setup_pusher(self):
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

    def getData(self):
        pass

    def unixToDatetime(self,unix_time):
        return datetime.fromtimestamp(int(unix_time))

    def graphIt(self):
        # get info from database
        c_time, grid, solarp = self.getData()
        # append info to a list for graph
        self.time.append(c_time)
        self.energy['solar_prod'].append(solarp)
        self.energy['grid_cons'].append(grid)
        # create a line graph

        # dump the data into json for transfering to front end

        # create trigger event
    
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
        self.energy = {'solarp':[], 'grid':[]}

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
            self.energy['grid'].append(g)
            self.energy['solarp'].append(s)
        
        # put the data into axis for Plotly
        grid_data = [go.Scatter(
            x=self.time,
            y=self.energy['grid'],
            name="Grid Consumption"
        )]
        solarp_data = [go.Scatter(
            x=self.time,
            y=self.energy['solarp'],
            name="Solar Plus"
        )]
        data = {
            'grid': json.dumps(list(grid_data), cls=plotly.utils.PlotlyJSONEncoder),
            'solarp': json.dumps(list(solarp_data), cls=plotly.utils.PlotlyJSONEncoder)
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