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