import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password='passord123'
)

cursor = db.cursor()

def setUpDatabase():
    pass

def addGame(game):
    pass

def addCompany(company):
    pass

def deleteDatabase():
    pass
