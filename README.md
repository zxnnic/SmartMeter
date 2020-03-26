# SmartMeter
For ECE 490 project, collect data from a PowerScout 3037S and process the data to create real-time visualizations

# Introduction

**There will be these major tasks:**

  * Database creation
  * Communication set up to the PowerScout
  * Storing data from the PowerScout to the database
  * Extracting the data from the database
  * Formatting the data so it can be used for graphing
  * Creating real-time/live plots

# Initial set up

Assuming that Python 3.0+ is on your device. 

1. Download MySQL, mysql connnector for Python, and create database called smart_meter_db

2. Install all the dependencies

       pip install -r requirements

3. Create a new file in the same folder named `db_settings_secret.py` and in that file paste the following

       """  
       These settings must never be uploaded onto github.

       Keep it secret
       """
       DB_USERNAME = "[Your_DB_Username]"

       DB_PASSWORD = "[enter your mysql root user password here]"
       
4. For pre-loaded data, create the following table:

       DROP TABLE IF EXISTS profiles;
       CREATE TABLE IF NOT EXISTS profiles (
        tstamp INTEGER NOT NULL,
        grid FLOAT, 
        solar FLOAT, 
        solarp FLOAT,  
        PRIMARY KEY (tstamp)
       );
   
   And insert your values in accordingly. 

5. Go into `app.py` to make sure that all the settings for your database is correct.

6. You first need to create a Pusher account so that real-time values can be fetched and the graphs can be updated. Go to https://pusher.com/ and create a free account.Then create a new channel with us3 cluster, the channel will give you the following information

       app_id = [your app id]
       key = [your key]
       secret = [your secret id]
       cluster = "us3"

7. Edit `app.py` and `graph_s.html` to your app id, key, and secret. 

# Launching the app

Step into the folder and run the following command on a terminal

       python realtime_db_simulator.py

Then open a separate terminal and run the command

       python app.py

Follow the link provided and the website will be available to you. :)


# Database Class usage

Database class has the following main methods

* `createTable(table_name, primary_key, opt_arguments)`
  * `table_name` : name of the table
  * `primary_key` : column name of the primary key
  * `opt_args` : other column names and their type in a tuple
  
          e.g. [('time', 'TIME'),
                ('current','FLOAT'),
                ('voltage','FLOAT'),
                ('phasor','FLOAT'),
                ('power','FLOAT')]
                
* `deleteTable(table_name)`
* `execute(query)`
   * Executes SQL commands returning `True` if completed successfully and `False` if not.
* `getQuery(query)`
   * Execute SQL query and returns an array of tuples containing row contents from the database
* `deleteRow(table_name, condition)`
* `deleteColumn(table_name, column_name)`
* `getHost()` - returns host as string
* `getPort()` - returns port as string
* `getDatabaseName()` - returns database name as string
* `isConnected()` - returns `True` is the connection to the database is made, and `False` if not.

To use the database class you just need to:
        
        db = Database(DB_USERNAME,
                        DB_PASSWORD,
                        'localhost', 
                        '3306',
                        'smart_meter_db')
        db.setup()
        
        #### do what ever you want to do
        
        db.close()
   
A more detailed example can be seen in the test section of `database.py`


       
