import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("Type password: ")
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
