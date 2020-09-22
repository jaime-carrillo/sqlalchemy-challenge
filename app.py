import numpy as np
import pandas as pd


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import  create_engine, func
import datetime as dt

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Station = Base.classes.station

Measurement = Base.classes.measurement

session = Session(engine)


app=Flask(__name__)


@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startdate<br/>"
        f"/api/v1.0/startdate/enddate<br/>"

        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= last_year).\
    order_by(Measurement.date).all()
    session.close()

    p = {date: prcp for date, prcp in precipitation}

    return jsonify(p)


@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()
    stations = list(np.ravel(stations))
    session.close()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():

    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    temp = session.query(Measurement.tobs).\
    filter(Measurement.station == "USC00519281").\
    filter(Measurement.date >= last_year).all()

    temp = list(np.ravel(temp))
    session.close()
    return jsonify(temp)

@app.route("/api/v1.0/<start>")
def temps(start): 

    temp = [func.min(Measurement.tobs),
       func.max(Measurement.tobs),
       func.avg(Measurement.tobs)]
    
    results = session.query(*temp).filter(Measurement.date >= start).all()

    results = list(np.ravel(results))
    session.close()
    return jsonify(results)


@app.route("/api/v1.0/<start>/<end>")
def temp_range(start,end):

    temp = [func.min(Measurement.tobs),
       func.max(Measurement.tobs),
       func.avg(Measurement.tobs)]
    
    results = session.query(*temp).filter(Measurement.date >= start).filter(Measurement.date <=end).all()

    results = list(np.ravel(results))
    session.close()
    return jsonify(results)
    


if __name__ == "__main__":
    app.run(debug=True)
