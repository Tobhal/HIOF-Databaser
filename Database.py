import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("Type password: ")
)

cursor = db.cursor()