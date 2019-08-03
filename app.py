#########################
# Import Dependencies
#########################
from flask import Flask,jsonify
import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#########################
# Database Setup
#########################

# create the engine object
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect the database/tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# savereferences to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#########################
# Flask Setup
#########################

app = Flask(__name__)

#########################
# Flask Routes
#########################

@app.route('/')
def home():
    return (
        f'Welcome to my Hawaiian climate app!<br/><br/>'
        f'Available routes:<br/>'
        f'------------------------------<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/[start_date]<br/>'
        f'/api/v1.0/[start_date]/[end_date]<br/><br/>'
        f'(use YYYY-MM-DD format for dates)'
    )



###################################
# Stations Route: List Stations
###################################

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)

    results = session.query(Station.name).all()

    # create a dictionary to return as json
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)



###########################################################################################
# Precipitation Route: return date and precip measurements for a year of the most recent dates
###########################################################################################

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)

    most_recent = session.query(func.max(Measurement.date)).all()
    most_recent_df = datetime.strptime(most_recent[0][0],'%Y-%m-%d')
    year_ago = most_recent_df - dt.timedelta(days = 365)
    year_ago_str = year_ago.strftime('%Y-%m-%d')

    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= year_ago_str).all()

    # create a dictionary to return as json
    precip = list(np.ravel(results))
    return jsonify(precip)



###############################################################################################
# TOBS Route: return date and temperature measurements for a year of the most recent dates
###############################################################################################

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)

    most_recent = session.query(func.max(Measurement.date)).all()
    most_recent_df = datetime.strptime(most_recent[0][0],'%Y-%m-%d')
    year_ago = most_recent_df - dt.timedelta(days = 365)
    year_ago_str = year_ago.strftime('%Y-%m-%d')

    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= year_ago_str).all()

    # create a dictionary to return as json
    tobs = list(np.ravel(results))
    return jsonify(tobs)


#########################################################################################################
# Start Date Route: return min, avg, and max temperature for every date after the start date, inclusive
#########################################################################################################

@app.route('/api/v1.0/<start>')
def start_date(start):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    # create a dictionary to return as json
    tobs = list(np.ravel(results))
    return jsonify(tobs)



#############################################################################################################################################
# Start Date and End Date Route: return min, avg, and max temperature for every date after the start date and before the end date, inclusive
#############################################################################################################################################

@app.route('/api/v1.0/<start>/<end>')
def start_and_end_date(start,end):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # create a dictionary to return as json
    tobs = list(np.ravel(results))
    return jsonify(tobs)  


################################
# Run the app
################################

if __name__ == '__main__':
    app.run(debug=True)



