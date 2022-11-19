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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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
# Homepage
def welcome():
    """All available routes"""
    # All routes
    return (
        f'Available routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end><br/>'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    # create session
    session = Session(engine)
    # query
    result1 = session.query(Measurement.date, Measurement.prcp).all()
    # close session
    session.close()

    # create list for precipitation measurements
    precip = []
    for date, prcp in result1:
        prcp_dict = {}
        prcp_dict[date] = prcp
        precip.append(prcp_dict)
        return jsonify(precip)


@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    result2 = session.query(Station.station).distinct().all()
    session.close()

    stations_list = list(np.ravel(result2))
    return jsonify(stations_list)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)

    
    session.close()
    return ()

@app.route('/api/v1.0/<start>')
def start_date():
    return ()

@app.route('/api/v1.0/<start>/<end>')
def start_end():
    return ()

if __name__ == '__main__':
    app.run(debug=True)
