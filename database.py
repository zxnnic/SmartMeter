########################################################
#
# This sets up the connection to the database
# You can open it in terminal and just run it to connect
# 
# This was made based on the code prvided by PYnative
# available at https://pynative.com/python-mysql-database-connection/ 
#
# Look in the bottom test section to see a simple implementation
#
########################################################

import mysql.connector
from mysql.connector import Error

class Database():
    def __init__(self, db_user, db_pass, db_host, db_port, db_name):
        self.__user = db_user
        self.__password = db_pass
        self.__host = db_host
        self.__port = db_port
        self.__name = db_name
        self.__connection = None
        self.__cursor = None

    def setup(self):
        '''
        Set up a connection and cursor to implement database actions
        if it fails throw an error message on the terminal
        '''
        try: 
            # initialize the connection
            self.__connection = mysql.connector.connect(host = self.__host,
                                        user= self.__user,
                                        port=self.__port,
                                        password = self.__password,
                                        database = self.__name)
            # set up autocommit
            self.__connection.autocommit = True
            # create a cursor
            self.__cursor = self.__connection.cursor()
            self.__cursor.execute("select database();")
            print("Connected to MySQL Server version ", self.__connection.get_server_info())
            print("You are connected to {}\n".format(self.__cursor.fetchone()[0]))
        except Error as err:
            print("ERROR:" + err)
        except Exception as err:
            print("ERROR:")
            for arg in err.args:
                print(arg)
        finally:
            return self.isConnected()
        
    def close(self):
            if self.isConnected():
                self.__cursor.close()
                self.__connection.close()
                print("MySQL connection is closed")

    def createTable(self, table_name, primary_key, opt_args=None):
        query = 'CREATE TABLE ' + table_name + '(' 
        if opt_args is not None:
            for arg in opt_args:
                query += arg[0] + ' ' + arg[1] + ','
        query += 'PRIMARY KEY (' + primary_key[0] + '));'

        if self.execute(query):
            print(table_name + ' successfully created.')
    
    def deleteTable(self, table_name):
        if self.execute('DROP TABLE ' + table_name +';'):
            print(table_name + ' successfully deleted.')

    def deleteRow(self, table_name, condition):
        query = 'DELETE FROM '+table_name+' WHERE '+condition
        if self.execute(query):
            print('Rows containing',condition,'in',table_name,'has been deleted.')
        
    def deleteColumn(self, table_name, column_name):
        query = 'ALTER TABLE '+table_name+' DROP COLUMN '+column_name
        if self.execute(query):
            print('Column', column_name, 'has been deleted.')
    
    def getQuery(self, query):
        '''
        arguments: query string in sql
        returns: list of tuples of table entries
        '''
        if self.execute(query):
            return self.__cursor.fetchall()

    def execute(self, query):
        '''
        Simple execution of sql commands
        arguments: query string
        returns: Boolean
        '''
        try:
            self.__cursor.execute(query)
        except Error as err:
            print(err)
            return False
        except Exception as err:
            print(err)
            return False
        else:
            return True

    def getHost(self):
        return self.__host
    
    def getPort(self):
        return self.__port
    
    def getDatabaseName(self):
        return self.__name
    
    def isConnected(self):
        return self.__connection.is_connected()


##########################################################################
########################## TESTING #######################################
##########################################################################
from db_settings_secret import *
import time
if __name__ == "__main__":
    # This is used to test out if the database can be connected
    db = Database(DB_USERNAME,
                        DB_PASSWORD,
                        'localhost', 
                        '3306',
                        'smart_meter_db')
    db.setup()
    # Test all the different functions offered by the database class
    # Perform the tasks that the user wants
    done = False
    while not done:
        print('Here are what you can do:')
        print('\t1) Create a new table')
        print('\t2) Delete a table')
        print('\t3) Insert into a table')
        print('\t4) Drop an entry from a table')
        print('\t5) Select command')
        print('\t6) Exit')

        user_input = int(input('What would you like to do? \n> '))
        if user_input == 1:
            # Each attribute/column of the table will need two parameters:
            #           (name, data type)
            primary_key = ('time', 'TIME')
            attributes = [  ('time', 'TIME'),
                            ('current','FLOAT'),
                            ('voltage','FLOAT'),
                            ('phasor','FLOAT'),
                            ('power','FLOAT')]
            db.createTable(table_name='energy_use', primary_key=primary_key, opt_args=attributes)
        elif user_input == 2:
            db.deleteTable('energy_use')
        elif user_input == 3:
            db.execute('insert into energy_use values (now(), 2.0, 120, 0.73, 240)')
            time.sleep(5)
            db.execute('insert into energy_use values (now(), 2.0, 120, 1, 120)')
        elif user_input == 4:
            db.deleteColumn('energy_use','current')
        elif user_input == 5:
            data = db.getQuery('select * from energy_use')
            print(type(data))
            for d in data:
                print(type(d))
        elif user_input == 6:
            done = True
            db.close()
            print('Good bye!')
        else:
            print('ERROR: You have entered an invalid number, please try again.\n')
