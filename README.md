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

# Initial database set up

1. Make sure you have Python 3, if not download it [HERE](https://www.python.org/downloads/)
2. Check if python is now in your path by running the following command in a terminal

       python 
   
   If python is not in your path, see where your Python files were stored and copy the path. For example if your Python files are stored at `C:\Program Files\Python\3.6\` then you can run the following command in a terminal
   
       set PATH [C:\Program Files\Python\3.6\lib]
       set PATH [C:\Program Files\Python\3.6\bin]
      
> NOTE: If you are having alot of trouble installing Python and would like a video tutorial please go to [HERE](https://www.youtube.com/watch?v=dNFgRUD2w68&t=859s) for Windows installation help.
      
3. Download PostgreSQL [HERE](https://www.postgresql.org/download/) and pgAdmin for easy user interfacing [HERE](https://www.pgadmin.org/download/). Set up your password and remember it, as it will be used for all future prostgresql access.
4. Check if you have pip installed by running in a terminal

       pip --version

    if pip is not installed please follow [this tutorial](https://www.youtube.com/watch?v=AVCcFyYynQY) to install

5. Now download the zip of all the github repo and unzip it.
6. In terminal, either 
    (1) step into the folder you stored the downloaded SmartMeter project in
    (2) Open the SmartMeter project folder in VS Code and open the terminal using `ctrl`+`shift`+`~`
    
    In the terminal run
    
       pip install -r requirements.txt
    
    This will install all the libraries used throughout the code.
7. Now create a new file in the same folder named `db_settings_secret.py` and in that file paste the following

       """  
       These settings must never be uploaded onto github.

       Keep it secret
       """
       DB_USERNAME = "[Your_DB_Username]"

       DB_PASSWORD = "[enter your postgresql password here]"

8. Open pgAdmin and create a new database, it will prompt you to type in your password. 
9. Once you are in, right click on `Databases` and click `Create` > `Database...`. 
10. A pop up window will appear an you can type in the database name as `smart_meter_db` and set the owner as your username.
11. Now go back to terminal and run the following command

        python setup.py

**CONGRATS! You are now connected**


       
