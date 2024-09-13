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