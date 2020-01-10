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

def setup():
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
        connection = psycopg2.connect(user = DB_USERNAME,
                                      password = DB_PASSWORD,
                                      host = '127.0.0.1',
                                      port = '5432',
                                      database = 'smart_meter_db')
        # create a cursor
        cursor = connection.cursor()
        # check 1: print postgres connection properties
        print ( connection.get_dsn_parameters(),"\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to ", record,"\n")
        print('Now you can continue on :^)\n')

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
                pass
            elif user_input == 2:
                pass
            elif user_input == 3:
                pass
            elif user_input == 4:
                pass
            elif user_input == 5:
                done = True
            else:
                print('ERROR: You have entered an invalid number, please try again.\n')

    except Exception as err:
        print("ERROR:")
        for arg in err.args:
            print(arg)
    finally:
        # close the connection no matter what
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")

def create_table(table_name):
    pass

def insert(table_name, id, value):
    pass

def delete(table_name, id):
    pass

def delete_table(table_name):
    pass


if __name__ == "__main__":
    setup()