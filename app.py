import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#homepage
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startdate<br/>"
        f"/api/v1.0/startdate/enddate<br/>"
        f"note: date format is %y-%m-%d"
    )

#precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of measurement data including the date and precipitation"""
    # Query date and prcp
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    prcp_date = []
    for date,prcp in results:
        dateprcp_dict = {}
        dateprcp_dict["date"] = date
        dateprcp_dict["precipitation"] = prcp
        prcp_date.append(dateprcp_dict)
    
    return jsonify(prcp_date)


#Stations
@app.route("/api/v1.0/stations")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations names"""
    # Query all statiion
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


#tobs
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #querey the data
    one_year = dt.date(2017, 8 ,23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs, Measurement.date).\
                  filter(Measurement.date >= one_year).filter(Measurement.station == "USC00519281").all()

    tobs_date = []
    for date,tobs in results:
        datetobs_dict = {}
        datetobs_dict["date"] = date
        datetobs_dict["TOBS"] = tobs
        tobs_date.append(datetobs_dict)
    
    return jsonify(tobs_date)


#start date
@app.route("/api/v1.0/<start_dt>",strict_slashes=False)
def vacation(start_dt):
     # Create our session (link) from Python to the DB
    session = Session(engine)
    #querey the data
    sel = [Measurement, 
       func.min(Measurement.tobs), 
       func.max(Measurement.tobs), 
       func.avg(Measurement.tobs)]
    
    temperature_start = session.query(*sel).\
    filter(Measurement.date > start_dt).all()

    session.close()
   
    # Convert list of tuples into normal list
    temperature_start = list(np.ravel(temperature_start))
    
    #dictionary!
    temp_start = {}
    temp_start["t_min"] = temperature_start[1]
    temp_start["t_max"] = temperature_start[2]
    temp_start["t_avg"] = temperature_start[3]


    return jsonify(temp_start)




#start date and end date
@app.route("/api/v1.0/<start_dt>/<end_dt>", strict_slashes=False)
def xyz(start_dt,end_dt):

# Create our session (link) from Python to the DB
    session = Session(engine)
    #querey the data
    sel = [Measurement, 
       func.min(Measurement.tobs), 
       func.max(Measurement.tobs), 
       func.avg(Measurement.tobs)]
    temperature_start_end = session.query(*sel).\
    filter(Measurement.date > start_dt).filter(Measurement.date < end_dt).all()

    session.close()
    temperature_start_end = list(np.ravel(temperature_start_end))

    temp_start_end = {}
    temp_start_end["t_min"] = temperature_start_end[1]
    temp_start_end["t_max"] = temperature_start_end[2]
    temp_start_end["t_avg"] = temperature_start_end[3]

    return jsonify(temp_start_end)



if __name__ == '__main__':
    app.run(debug=True)