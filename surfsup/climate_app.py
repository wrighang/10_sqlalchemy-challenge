# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#added Path
from pathlib import Path
#added to preserve order of keys in dictionaries 
from collections import OrderedDict 

#################################################
# Database Setup
#################################################
hawaii_database_path = Path("../resources/hawaii.sqlite")

## create engine to hawaii.sqlite
engine = create_engine(f"sqlite:///{hawaii_database_path}").connect()

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all the available api routes"""
    return (
        f"Welcome to the Hawaii Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/&lt;start_date&gt; (ie: /api/v1.0/start/2016-09-01)<br/>"
        f"/api/v1.0/start_end/&lt;start_date&gt;_&lt;end_date&gt; (ie: /api/v1.0/start_end/2010-10-10_2010-12-24)<br/>"
    )


"""Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
    Return the JSON representation of your dictionary"""
@app.route("/api/v1.0/precipitation")
def precipitation():
                        
        # Find the most recent date in the data set.
        most_recent_date = session.query(func.max(Measurement.date)).scalar()
    
        if most_recent_date is None:
            return jsonify({"error": "No data available."}), 404
        

        #convert string to datetime object
        # Calculate the date one year from the last date in data set.
        #one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)
        
        # Perform a query to retrieve the data and precipitation scores -- using one_year_ago 
        precip_scores = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= one_year_ago)\
            .order_by(Measurement.date)\
            .all()

        session.close()
        
        #create a dictionary
        all_prcp = [{f"date": date, f"prcp": prcp} 
                    for date, prcp in precip_scores]
               
        return jsonify(all_prcp)

"""Return a JSON list of stations from the dataset"""
@app.route("/api/v1.0/stations")
def stations():
            
            #query all stations                
            query_stations = session.query(Station.station).all()

            # Convert list of tuples into normal list
            all_stations = list(np.ravel(query_stations))

            session.close()

            return jsonify(all_stations)
    
"""Query the dates and temperature observations of the most-active station for the previous year of data.
Return a JSON list of temperature observations for the previous year"""        
@app.route("/api/v1.0/tobs")
def temp():
                        
            # Using the most active station id from the previous query, calculate the lowest, highest, and average temperature.
            most_active = session.query(Measurement.station, func.count(Measurement.station))\
                    .group_by(Measurement.station)\
                    .order_by(func.count(Measurement.station).desc())\
                    .first()

            #extract the station ID from the tuple
            most_active_station_id = most_active[0]

            # Find the most recent date in the data set.
            most_recent_date = session.query(func.max(Measurement.date)).first()[0]

            # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
            # Starting from the most recent data point in the database. 
            #convert string to datetime object
            most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d').date()

            # Calculate the date one year from the last date in data set.
            #one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
            one_year_ago = most_recent_date - dt.timedelta(days=365)

            # Query the last 12 months of temperature observation data for this station and plot the results as a histogram
            temp_obs = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.station == most_active_station_id).\
                filter(Measurement.date >= one_year_ago).all()

            session.close()
            
            #create a list of dictionaries for the JSON response
            all_temp_obs = [{f"date": date, f"temperature": tobs} 
                            for date, tobs in temp_obs]
                                    
            return jsonify(all_temp_obs)

"""Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start date.
For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date."""
###Example used to check http://127.0.0.1:5000/api/v1.0/start/2016-09-01
####Example used to check no results http://127.0.0.1:5000/api/v1.0/start/2024-12-03
@app.route("/api/v1.0/start/<start_date>")
def start_route(start_date):
        
        #convert start to datetime
        start_date_route = dt.datetime.strptime(start_date,'%Y-%m-%d').date()

        #query the min, avg, and max temperatures from the start date
        start_query = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
        ).filter(Measurement.date >= start_date_route).all()

        session.close()

    #check if results are found
        if start_query[0][0] is None:
            return jsonify({"error": f"No data found for the specified date {start_date}."}), 404

        #extract the data from the result
        min_temp, avg_temp, max_temp = start_query[0]

        # Create a dictionary to hold the results
        temp_data = {
            "start date": start_date,
            "TMIN": min_temp,
            "TAVG": round(avg_temp,1),
            "TMAX": max_temp}

        return jsonify(temp_data)

"""Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range.
For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive."""
###Example used to check http://127.0.0.1:5000/api/v1.0/start_end/2010-10-10_2010-12-24
####Example used to check no results http://127.0.0.1:5000/api/v1.0/start_end/2024-11-01_2024-11-15 
@app.route("/api/v1.0/start_end/<start>_<end>")
def start_end_route(start, end):

        #convert start to datetime
            start_date = dt.datetime.strptime(start,'%Y-%m-%d').date()
            end_date = dt.datetime.strptime(end, '%Y-%m-%d').date()

            #calculate the lowest, highest, and average temperature for the dates from the start date to the end date
            start_end_query = session.query(
                            func.min(Measurement.tobs),
                            func.avg(Measurement.tobs),
                            func.max(Measurement.tobs)
                        ).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

            session.close()
            
        #check if results are found
            if start_end_query[0][0] is None:
                return jsonify({"error": f"No data found for the specified date range {start} to {end}"}), 404
            
            # Extract the data from the result
            min_temp, avg_temp, max_temp = start_end_query[0]
        
            # Create a dictionary to hold the results
            temp_data = {
                "start date": start,
                "end date": end,
                "TMIN": min_temp,
                "TAVG": round(avg_temp,1),
                "TMAX": max_temp}
            
            return jsonify(temp_data)

if __name__ == '__main__':
    app.run(debug=True)