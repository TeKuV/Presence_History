import serial
import time
import sqlite3
from datetime import datetime
from time import strftime

#database = "F:\\Personnals\\Projects\\Python\\Python_Arduino\\user_info.db"
database = ".\\database\\user_info.db"

def connect_db(database):
    try:
        connection = sqlite3.connect(database)
        return connection, connection.cursor()
    except Error as e:
        print(e)

def logging(user_id, user_name):
    
    connection, cursor = connect_db(database)
    
    find_user = ('SELECT * FROM user WHERE  id = ? AND name = ?')
    cursor.execute(find_user, [(user_id), (user_name)])

    results = cursor.fetchall()

    if results:
        for user in results:
            print("\n--------------------------------------------\n")
            print("welcome ", user[1])

            #getting connection time after authentification
            _date_time = str(datetime.now())
            date_time = _date_time.split(" ")
            _date = date_time[0]
            _time = date_time[1]

            try:
                insert_date_time = ('INSERT INTO tagge (jour, heure, id) VALUES (?, ?, ?)')
                cursor.execute(insert_date_time, (_date, _time, user_id))
                
                connection.commit()
                print("Data upload")
            except :
                print("Could not add time information to the database !!")


    else:
        print("\n--------------------------------------------\n")
        print("Card is not define ! Contact the administrator")

    connection.close()

def user_cart_info():
    try:
        com = serial.Serial("COM3", 9600)
    
    except PermissionError as p:
        print("Permission denied to the baude")
        return

    chars = []

    while True:
        char = com.readline().decode('utf-8')

        if char != '\r\n':
            chars.append(char)
        else:
            break
    #User ID
    temp = chars[2].split("Card UID: ")
    _id = temp[1].split('\r\n')

    # Name
    _name = chars[6].split('  ')

    return (_id[0], _name[0])

def run_server():
    print("Starting serial server...")

    while True:
        #get cart informations
        user_id, user_name = user_cart_info()

        #test if user exit and if his has the acces
        logging(user_id,user_name)

run_server()