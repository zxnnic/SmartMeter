########################################################
#
# This sets up the connection to the database
# You can open it in terminal and just run it to connect
#
########################################################
import psycopg2
import db_settings_secret

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
        connection = psycopg2.connect(user = username,
                                      password = password,
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
        print("You are connected to - ", record,"\n")
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

if __name__ == "__main__":
    setup()