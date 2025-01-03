# 10_sqlalchemy-challenge

[Climate Analysis.ipynb](https://github.com/wrighang/10_sqlalchemy-challenge/blob/main/surfsup/climate_analysis.ipynb)

[Climate App.py](https://github.com/wrighang/10_sqlalchemy-challenge/blob/main/surfsup/climate_app.py)

## Instructions
Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area. The following outlines the requirements for this assignment.

# Requirements

## Jupyter Notebook Database Connection
To receive full credit, you must:
- Use the SQLAlchemy `create_engine()` function to connect to your SQLite database.
- Use the SQLAlchemy `automap_base()` function to reflect your tables into classes.
- Save references to the classes named `station` and `measurement`.
- Link Python to the database by creating a SQLAlchemy session.
- Close your session at the end of your notebook.

## Precipitation Analysis
To receive full credit, you must:
- Create a query that finds the most recent date in the dataset (`8/23/2017`).
- Create a query that collects only the date and precipitation for the last year of data without passing the date as a variable.
- Save the query results to a Pandas DataFrame to create `date` and `precipitation` columns.
- Sort the DataFrame by date.
- Plot the results by using the DataFrame plot method with `date` as the x and `precipitation` as the y variables.
- Use Pandas to print the summary statistics for the precipitation data.

## Station Analysis
To receive full credit, you must:
- Design a query that correctly finds the number of stations in the dataset.
- Design a query that correctly lists the stations and observation counts in descending order and finds the most active station (`USC00519281`).
- Design a query that correctly finds the min, max, and average temperatures for the most active station (`USC00519281`).
- Design a query to get the previous 12 months of temperature observation (`TOBS`) data that filters by the station that has the greatest number of observations.
- Save the query results to a Pandas DataFrame.
- Correctly plot a histogram with `bins=12` for the last year of data using `tobs` as the column to count.

## API SQLite Connection & Landing Page
To receive full credit, your Flask application must:
- Correctly generate the engine to the correct sqlite file.
- Use `automap_base()` and reflect the database schema.
- Correctly save references to the tables in the sqlite file (`measurement` and `station`).
- Correctly create and bind the session between the Python app and database.
- Display the available routes on the landing page.

## API Static Routes
To receive full credit, your Flask application must include:
- A precipitation route that:
  - Returns JSON with the date as the key and the value as the precipitation.
  - Only returns the JSONified precipitation data for the last year in the database.
- A stations route that:
  - Returns JSONified data of all of the stations in the database.
- A tobs route that:
  - Returns JSONified data for the most active station (`USC00519281`).
  - Only returns the JSONified data for the last year of data.

## API Dynamic Route
To receive full credit, your Flask application must include:
- A start route that:
  - Accepts the start date as a parameter from the URL.
  - Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset.
- A start/end route that:
  - Accepts the start and end dates as parameters from the URL.
  - Returns the min, max, and average temperatures calculated from the given start date to the given end date.

## Coding Conventions and Formatting
To receive full credit, your code must:
- Place imports at the top of the file, just after any module comments and docstrings, and before module globals and constants.
- Name functions and variables with lowercase characters, with words separated by underscores.
- Follow DRY (Don't Repeat Yourself) principles, creating maintainable and reusable code.
- Use concise logic and creative engineering where possible.

## Deployment and Submission
To receive full credit, you must:
- Submit a link to a GitHub repository that’s cloned to your local machine and contains your files.
- Use the command line to add your files to the repository.
- Include appropriate commit messages in your files.

## Comments
To receive full credit, your code must:
- Be well commented with concise, relevant notes that other developers can understand.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## CODING_PROCESS

Overall Approach

- Referenced activity assignments and Xpert Learning Assistant for guidance throughout the challenge, paying close attention to proper indentation in the Climate App code. Some areas of guidance listed below:

- Climate Analysis

* Looked up how to convert strings to datetime objects for date calculations, ensuring accurate implementation of code. For example, 
one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

* Used SQL queries with Pandas to inspect database tables. For example: data = pd.read_sql("SELECT * FROM measurement", engine)

* Referenced activities to calculate min, max, and average temperatures and reviewed histogram plotting for visualizations.

* Looked up how to create the temperate symbol (option + shift + 8 = °)

- Climate App

* Researched how to structure 404 error messages. For example:    
    if most_recent_date is None:
                return jsonify({"error": "No data available."}), 404

* The wording for the /start and /start_end routes was initially confusing, so I clarified these requirements using Xpert Learning Assistant. I provided examples in the landing page response to guide users. For example: /api/v1.0/start_end/2010-10-10_2010-12-24
