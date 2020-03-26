from mysql.connector import Error
from database import Database
from db_settings_secret import *

import time


def simulator():
    # set up database
    db = Database(DB_USERNAME,
                    DB_PASSWORD,
                    '127.0.0.1', 
                    '3306',
                    'smart_meter_db')
    db.setup()

    # create new table
    db.execute('''DROP TABLE IF EXISTS e_sim;''')
    db.execute('''
            CREATE TABLE e_sim (
                tstamp	int(11),
                grid	float,
                solarp	float,
                PRIMARY KEY (tstamp)
            );''')

    # Extract all the data that we will graph
    time_interval = 15
    limit=1000*time_interval
    data = db.getQuery('''
                            SELECT p.tstamp, p.grid, p.solarp
                            FROM (
                                SELECT @row := @row +1 AS rownum, tstamp, grid, solarp
                                FROM (SELECT @row :=0) r, profiles
                                LIMIT {0}
                            ) p
                            WHERE p.rownum % {1} = 0
                        '''.format(limit,time_interval))
    
    # insert data one at a time
    for row in data:
        db.execute("INSERT INTO e_sim VALUES "+str(row))
        print('inserting '+str(row)+' into the database')
        time.sleep(1)

if __name__ == "__main__":
    simulator()