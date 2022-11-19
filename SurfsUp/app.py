# Import dependencies
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Flask
from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Setup Flask
app = Flask(__name__)

# Flask routes
@app.route('/')
# Start at the homepage
def welcome():
    """All available routes"""
    # List all the available routes
    return (
        f'Available routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start>yyyy-mm-dd<br/>'
        f'/api/v1.0/<start>yyyy-mm-dd/<end>yyyy-mm-dd<br/>'
    )


# Route 1 '/api/v1.0/precipitation'
# Convert the query results from your precipitation analysis 
# (i.e. retrieve only the last 12 months of data) 
# to a dictionary using date as the key and prcp as the value.
@app.route('/api/v1.0/precipitation')
def precipitation():
    # create session
    session = Session(engine)
    # query
    query1 = session.query(Measurement.date, Measurement.prcp).all()
    # close session
    session.close()

# Return the JSON representation of your dictionary
    # create list for precipitation measurements
    precip = []
    for date, prcp in query1:
        prcp_dict = {}
        prcp_dict[date] = prcp
        precip.append(prcp_dict)
    return jsonify(precip)


# Route 2 '/api/v1.0/stations'
# Return a JSON list of stations from the dataset.
@app.route('/api/v1.0/stations')
def stations():
    # create session
    session = Session(engine)
    query2 = session.query(Station.station).distinct().all()
    session.close()

    stations_list = list(np.ravel(query2))
    return jsonify(stations_list)


# Route 3 '/api/v1.0/tobs'
# Query the dates and temperature observations of the most-active 
# station for the previous year of data.
@app.route('/api/v1.0/tobs')
def tobs():
    # create session
    session = Session(engine)
    
    # obtain most recent date 
    recent_date = dt.date(2017,8,23)
        
    # obtain query date
    q_date = recent_date - dt.timedelta(days = 365)
    # query the date and temperature observations
    query3 = session.query(
        Measurement.date, 
        Measurement.prcp
        ).filter(
            Measurement.date >= q_date
            ).all()
    
    # close session
    session.close()

# Return a JSON list of temperature observations for the previous year.
    tobs_list = []
    for date, tobs in query3:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)


# Route 4 '/api/v1.0/<start>' and '/api/v1.0/<start>/<end>'
# Return a JSON list of the minimum temperature, the average temperature, 
# and the maximum temperature for a specified start or start-end range.
@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def between_dates(start, end = None):
    # create session
    session = Session(engine)

# For a specified start, calculate TMIN, TAVG, and TMAX for all the 
# dates greater than or equal to the start date.
    if end is None:
        end = session.query(func.max(Measurement.date)).first()[0]

# For a specified start date and end date, calculate TMIN, TAVG, and TMAX 
# for the dates from the start date to the end date, inclusive.
    q_tobs = session.query(
        Measurement.date, 
        Measurement.tobs
        ).filter(Measurement.date >= start
        ).filter(Measurement.date <= end)
 
    tobs_df = pd.DataFrame(q_tobs, columns=['date', 'tobs'])

    # close session
    session.close()

    return f"The temperature analysis between the dates {start} and {end}: \n\
        Minimum: {tobs_df['tobs'].min()} F, \n\
        Maximum: {tobs_df['tobs'].max()} F, \n\
        Average: {tobs_df['tobs'].mean()} F."


if __name__ == '__main__':
    app.run(debug=True)