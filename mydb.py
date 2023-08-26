import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'root',
)

# create a cursor object 
cursorObject = dataBase.cursor();

# create the database
cursorObject.execute('CREATE DATABASE crmdb')

print('Database created !!')