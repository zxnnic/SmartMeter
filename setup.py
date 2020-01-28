########################################################
#
# This sets up the connection to the database
# You can open it in terminal and just run it to connect
# 
# This was made based on the code prvided by PYnative
# available at https://pynative.com/python-postgresql-tutorial/
#
########################################################
import psycopg2
from db_settings_secret import *

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
        Set up with the following parameters:
            username: ** in secret settings file **
            password: ** in secret settings file **
            hostname: 127.0.0.1
            port: 5432 
                (if 5432 is not available use the following command
                in the terminal 
                    netstat -an |find /i "listening"
                to find any available port on your device
                )

        if it fails throw an error message on the terminal
        '''
        try: 
            # initialize the connection
            self.connection = psycopg2.connect(user = self.__user,
                                        password = self.__password,
                                        host = self.__host,
                                        port = self.__port,
                                        database = self.__name)
            # create a cursor
            self.cursor = self.connection.cursor()

            # Check 1: print postgres connection properties
            # uncomment the print to see details
            # print (self.connection.get_dsn_parameters(),"\n")
            # Check 2: PostgreSQL version
            # self.cursor.execute("SELECT version();")
            # record = self.cursor.fetchone()
            # print(record)
        except psycopg2.Error as err:
            print("ERROR:" + err)
        except Exception as err:
            print("ERROR:")
            for arg in err.args:
                print(arg)
        else:
            print("You are connected to", self.connection.get_dsn_parameters()['dbname'])
            print('Now you can continue on :^)\n')
            return True
        
    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed.")

    def createTable(self, table_name, primary_key, opt_args=None):
        query = 'CREATE TABLE ' + table_name + '(' + primary_key[0] +' '+ primary_key[1] + ' NOT NULL,'
        if opt_args is not None:
            for arg in opt_args:
                query += arg[0] + ' ' + arg[1] + ','
        query += 'PRIMARY KEY (' + primary_key[0] + '));'

        if self.execute(query):
            print(table_name + ' successfully deleted.')
    
    def deleteTable(self, table_name):
        if self.execute('DROP TABLE ' + table_name +';'):
            print(table_name + ' successfully deleted.')

    def deleteRow(self, table_name, condition):
        if self.execute('DELETE FROM',table_name,'WHERE',condition):
            print('Rows containing',condition,'in',table_name,'has been deleted.')

    def insert(self, table_name, columns, values):
        # This method is still in question as of whether or not it should be kept
        # I am not sure if we even need the insert function
        query = 'INSERT INTO '+ table_name +' ('
        for column in columns:
            query += column +','
        query += ') VALUES ('
        for value in values:
            query += value + ','
        query += ');'
        
        if self.execute(query):
            print('Items successfully inserted into',table_name)

    def deleteColumn(self, table_name, column_name):
        if self.execute('ALTER TABLE', table_name, 'DROP COLUMN', column_name):
            print('Column', column_name, 'has been deleted.')
    
    # '''THESE TWO FUNCTIONS STILL ARE UNDER REVIEW'''
    # def getColumn(self, column, table_name, condition=None):
    #     query = 'SELECT ' + column + ' FROM ' +table_name
    #     if condition is not None:
    #         query += 'WHERE ' + 
    
    # def getTable(self, table_name):
    #     query = 'SELECT * FROM ' + table_name +';'
    # ''''''

    def execute(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as err:
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

if __name__ == "__main__":
    # This is used to test out if the database can be connected
    db = Database(DB_USERNAME,
                        DB_PASSWORD,
                        '127.0.0.1', 
                        '5432',
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
        print('\t5) Exit')

        user_input = int(input('What would you like to do? \n> '))
        if user_input == 1:
            # Each attribute/column of the table will need two parameters:
            #           (name, data type)
            primary_key = ('time', 'TIME')
            attributes = [  ('current','FLOAT'),
                            ('voltage','FLOAT'),
                            ('phasor','FLOAT'),
                            ('power','FLOAT')]
            db.createTable(table_name='energy_use', primary_key=primary_key, opt_args=attributes)
        elif user_input == 2:
            db.deleteTable('energy_use')
        elif user_input == 3:
            db.insert('hehe',1,'hellow')
        elif user_input == 4:
            db.delete('hehe', 12)
        elif user_input == 5:
            done = True
        else:
            print('ERROR: You have entered an invalid number, please try again.\n')
