import mysql.connector

def setUpDatabase():
    pass

def addGame(game):
    pass

def addCompany(company):
    pass

def deleteDatabase():
    pass

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("Type password: ")
)

cursor = db.cursor()