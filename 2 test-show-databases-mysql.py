# Ejecutar ▶
# pip install mysql-connector-python

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
)

cursor = db.cursor()

cursor.execute("SHOW DATABASES")

print(cursor.fetchall())