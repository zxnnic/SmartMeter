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


       
