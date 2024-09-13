# Code test for data engineering candidates

## Purpose

This test is designed to showcase your understanding of databases and data processing, together with your aptitude in a programming language of your choice.

There are two stages to this code test:

1. Preparing code at home ahead of your interview.
2. Pairing with us at the interview, making additions to your code.

The pairing phase is to give us an indication of what it will be like to work together, and should be regarded as a collaborative effort.

## Prerequisites

- Knowledge of relational databases, including how to create tables, insert data, and query data. For the purpose of this test, we are using MySQL.
- Knowledge of a programming language, including how to read and write files, process data, and access a MySQL database.
- Familiarity with Docker for container management, which we use through the Docker Compose tool. You will need Docker and Docker Compose installed on your development machine.
- Familiarity with Git for source control, and a github.com account which will be used for sharing your code.
- Zoom, which we will use for the pairing.

We have included example data and programme code. The example schema creates a simple table, with example code in several common programming languages to load data from a CSV file and output to a JSON file. There are instructions towards the bottom of this document explaining how to use the Docker containers, start the database, and use the examples.

## Background

We have provided a Github repo containing:

- A **docker compose.yml** file that configures a container for the MySQL database, and the example scripts’ containers.
- An **images** folder containing example programmes showing how the database can be accessed from C, Node, Python, R, Ruby, and Swift.
- An **example_schema.sql** file containing a table schema used by the example scripts.
- A **data** folder containing four files:
  - **example.csv** A tiny dataset, used by the example scripts.
  - **places.csv** 113 rows, where each row has a city, county, and country name.
  - **people.csv** 10,000 rows, where each row has a first name, last name, date of birth, and city of birth.
  - **sample_output.json** Sample output file, to show what your output should look like.

## Problem

There are a sequence of steps that we would like you to complete. We hope this won't take more than a couple of hours of your time.

1. Fork the git repo to your own Github account.
2. Devise a database schema to hold the data in the people and places CSV files, and apply it to the MySQL database. You may apply this schema via a script, via the MySQL command-line client, or via a GUI client.
3. Create a Docker image for loading the CSV files, places.csv and people.csv, into the tables you have created in the database. Make sure the appropriate config is in the docker compose file. Your data ingest process can be implemented in any way that you like, as long as it runs within a Docker container. You may implement this via programme code in a language of your choice, or via the use of ETL tools.
4. Create a Docker image for outputting a summary of content in the database. You may implement this using a programming language of your choice. The output must be in JSON format, and be written to a file in the data folder called **data/summary_output.json**. It should consist of a list of the countries, and a count of how many people were born in that country. We have supplied a sample output **data/sample_output.json** to compare your file against.
5. Share a link to your cloned github repo with us so we can review your code ahead of your interview.

We have provided an example schema and code that shows how to handle a simple data ingest and output.

Details of how to run and connect to the database are below, together with how to use the example schema and code.

## Solution for this assignment

### Create SQL Script for Schema

First, create a file called schema.sql that contains the SQL statements to create your places and people tables.

schema.sql:
```
CREATE TABLE IF NOT EXISTS places (
  id INT AUTO_INCREMENT PRIMARY KEY,
  city VARCHAR(100),
  county VARCHAR(100),
  country VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS people (
  id INT AUTO_INCREMENT PRIMARY KEY,
  given_name VARCHAR(100),
  family_name VARCHAR(100),
  date_of_birth DATE,
  place_of_birth VARCHAR(100)
);
```

### Create docker-compose.yml for mysql database, data_loader and summary_output

```
services:
  database:
    image: mysql
    environment:
      - MYSQL_RANDOM_ROOT_PASSWORD=yes
      - MYSQL_DATABASE=codetest
      - MYSQL_USER=codetest
      - MYSQL_PASSWORD=swordfish
    ports:
      - "3306:3306"
    volumes:
      - ./schema.sql:/docker-entrypoint-initdb.d/schema.sql
    restart: always

  data_loader:
    build: ./data_loader
    depends_on:
      - database

  summary_output:
    build: ./summary_output
    depends_on:
      - database
    volumes:
      - ./output:/app/output
```

### Create data loader Dockerfile and python script

Dockerfile
```
FROM python:3.8-slim
WORKDIR /app
COPY ./data /app/data
COPY ./load_data.py /app/load_data.py
RUN pip install mysql-connector-python pandas
CMD ["python", "load_data.py"]
```

load_data.py
```
import pandas as pd
import mysql.connector

# MySQL connection
connection = mysql.connector.connect(
    host='database', user='codetest', password='swordfish', database='codetest'
)
cursor = connection.cursor()

# Load places.csv
places_df = pd.read_csv('data/places.csv')
for _, row in places_df.iterrows():
    cursor.execute(
        "INSERT INTO places (city, county, country) VALUES (%s, %s, %s)", 
        (row['city'], row['county'], row['country'])
    )
connection.commit()

# Load people.csv
people_df = pd.read_csv('data/people.csv')
for _, row in people_df.iterrows():
    cursor.execute(
        "INSERT INTO people (given_name, family_name, date_of_birth, place_of_birth) VALUES (%s, %s, %s, %s)", 
        (row['given_name'], row['family_name'], row['date_of_birth'], row['place_of_birth'])
    )
connection.commit()
cursor.close()
connection.close()
```

### Create summary output Dockerfile and python script

Dockerfile
```
FROM python:3.8-slim
WORKDIR /app
COPY ./output_summary.py /app/output_summary.py
RUN pip install mysql-connector-python
CMD ["python", "output_summary.py"]
```

output_summary.py
```
import mysql.connector
import json

# Connect to MySQL
connection = mysql.connector.connect(
    host='database',  # This refers to the container name or host name
    user='codetest',
    password='swordfish',
    database='codetest',
    port=3306  # Specify the port number here
)
cursor = connection.cursor()

# Query to count people by country
query = """
    SELECT p.country, COUNT(pe.id) as count
    FROM people pe
    JOIN places p ON pe.place_of_birth = p.city
    GROUP BY p.country;
"""
cursor.execute(query)
result = cursor.fetchall()

# Format result into JSON
output = [{"country": row[0], "count": row[1]} for row in result]

with open('/app/output/summary_output.json', 'w') as f:
    json.dump(output, f, indent=4)

cursor.close()
connection.close()
```

### Building the images

This will build all of the images referenced in the Docker Compose file. You will need to re-run this after making code changes. (You can also specify individual services to build if that is more convenient.)

```
docker compose build
```

### Starting MySQL

To start up the MySQL database. This will will take a short while to run the database’s start-up scripts.

```
docker compose up database
```

Optional: if you want to connect to the MySQL database via the command-line client. This may be useful for looking at the database schema or data.

```
docker compose run database mysql --host=database --user=codetest --password=swordfish codetest
```

### Starting Data Loader

Running data loader to load the csv file to tables.

```
docker compose run data_loader
```

### Starting Summary Output

Running python script to generate a summary JSON output with the count of people born in each country

```
docker compose run summary_output
```

### Cleaning up

To tidy up, bringing down all the containers and deleting them.

```
docker compose down
```


