# Ejecutar ▶
# pip install mysql-connector-python
 
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=""
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE prueba")