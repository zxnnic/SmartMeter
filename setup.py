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
            # check 1: print postgres connection properties
            print ( self.connection.get_dsn_parameters(),"\n")

            # Print PostgreSQL version
            self.cursor.execute("SELECT version();")
            record = self.cursor.fetchone()
        except Exception as err:
            print("ERROR:")
            for arg in err.args:
                print(arg)
        else:
            print("You are connected to ", record,"\n")
            print('Now you can continue on :^)\n')
            return True
        
    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed.")

    def create_table(self, table_name):
    pass

    def insert(self, table_name, id, value):
        pass

    def delete(self, table_name, id):
        pass

    def delete_table(self, table_name):
        pass

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
            db.create_table('hehe')
        elif user_input == 2:
            db.delete_table('hehe')
        elif user_input == 3:
            db.insert('hehe',1,'hellow')
        elif user_input == 4:
            db.delete('hehe', 12)
        elif user_input == 5:
            done = True
        else:
            print('ERROR: You have entered an invalid number, please try again.\n')

