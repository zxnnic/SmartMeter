from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from graph import graph
import atexit

# create flask app
app = Flask(__name__)

# set up route to template
@app.route("/")
def index():
    return render_template("index.html")

# create schedule for retrieving prices
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=graph,
    trigger=IntervalTrigger(seconds=10),
    id='get_energy',
    name='Retrieve solar energy produced every 10 seconds',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
##### also shut down the database connection!!!
# run Flask app
app.run(debug=True, use_reloader=False)