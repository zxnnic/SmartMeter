##################################################
#
# This is functions that storing into database 
# functions will use. 
#
#################################################

from database import Database

def db_setup():
    '''
    Sets up a connection to the database with all the tables created
    
    Returns the database object
    '''
    # This is used to test out if the database can be connected
    db = Database(DB_USERNAME,
                        DB_PASSWORD,
                        'localhost', 
                        '3306',
                        'smart_meter_db')
    db.setup()
    # create the tables
    db.execute('''
                CREATE TABLE e_consume (
                    time        TIME,
                    current     INT,
                    apprnt_pwr  INT,
                    actv_pwr    INT,
                    rct_pwr     INT,
                    PRIMARY KEY (time),
                );
                CREATE TABLE e_source (
                    id          CHAR(10),
                    type        CHAR(20),
                    PRIMARY KEY (id)
                )
                ''')
    
    return db