# Import Dependencies
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct, inspect

# Set-Up Session
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    print("Homepage Request")
    return(
        f"Welcome to your Weather Report<br/>"
        f"Available Routes<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date]<br/>"
        f"/api/v1.0/[start_date]/[end_date]<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("PRCP Request")
    all_dates = []
    results = session.query(Measurement).all()
    for msmt in results:
        measurement_dict = {}
        measurement_dict[msmt.date] = msmt.prcp
        all_dates.append(measurement_dict)
    
    return(jsonify(all_dates))

@app.route("/api/v1.0/stations")
def stations():
    print("STATION Request")
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    
    return(jsonify(stations))

@app.route("/api/v1.0/tobs")
def tobs():
    print("TOBS Request")
    results = session.query(Measurement.tobs).filter(Measurement.date >= "2016-08-23").all()
    tobs = list(np.ravel(results))

    return(jsonify(tobs))

@app.route("/api/v1.0/<start_date>")
def start_stats(start_date):
    minimum = session.query(Measurement.tobs, func.min(Measurement.tobs)).filter(Measurement.date >= start_date)
    maximum = session.query(Measurement.tobs, func.max(Measurement.tobs)).filter(Measurement.date >= start_date)
    average = session.query(Measurement.tobs, func.avg(Measurement.tobs)).filter(Measurement.date >= start_date)

    start_temp = {"Tmin": minimum[0][0], "Tmax": maximum[0][0], "Tavg": average[0][0]}
    
    
    return jsonify(start_temp)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start(start_date, end_date):
    #When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."
    minimum = session.query(Measurement.tobs, func.min(Measurement.tobs)).filter(Measurement.date.between(start_date, end_date))
    maximum = session.query(Measurement.tobs, func.max(Measurement.tobs)).filter(Measurement.date.between(start_date, end_date))
    average = session.query(Measurement.tobs, func.avg(Measurement.tobs)).filter(Measurement.date.between(start_date, end_date))

    start_end_temps = {"Tmin": minimum[0][0], "Tmax": maximum[0][0], "Tavg": average[0][0]}
    
    return jsonify(start_end_temps)

if __name__ == "__main__":
    app.run(debug=True)