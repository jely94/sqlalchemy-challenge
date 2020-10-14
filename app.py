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
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the JSON representation of your dictionary."""

    # Calculate the date 1 year ago from the last data point in the database
    query_date = dt.date(2017, 8, 23)- dt.timedelta(days=364)

    # Quering the highest precipitation score per day and then grouping by that date
    one_year_precip = session.query(measurement.date, func.max(measurement.prcp)).\
                        filter(measurement.date >= query_date).group_by(measurement.date).all()

    # Convert to list of dictionaries to jsonify
    precip_data = []

    for date, prcp in one_year_precip:
        precip_dict = {}
        precip_dict[date] = prcp
        precip_data.append(precip_dict)

    session.close()

    return jsonify(precip_data)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset."""

    # Query all passengers
    station_list = session.query(station.name).all()

    # Convert list of tuples into normal list
    stations = list(np.ravel(station_list))

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():   
    # Create our session from Python to the DB
    session = Session(engine)

    """Return a JSON list of temperature observations (TOBS) for the previous year."""

    #Calculate the date 12 months prior to the last date of data recorded (2017-08-23)
    query_date = dt.date(2017, 8, 23)- dt.timedelta(days=364)



@app.route("/api/v1.0/start")
def start():   
    # Create our session from Python to the DB
    session = Session(engine)

    
@app.route("/api/v1.0/start/end")
def start_end():   
    # Create our session from Python to the DB
    session = Session(engine)


if __name__ == '__main__':
    app.run(debug=True)