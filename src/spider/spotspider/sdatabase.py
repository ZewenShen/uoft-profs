import pymysql
import sys


def __get_params(path):
    """
    get the information about database path, username, password, etc.
    """
    f = open(path, 'r')
    params = f.readlines()
    f.close()
    params = [item.strip('\n') for item in params]
    params[3] = int(params[3])
    return params

def init_db(path, DB_NAME): # Should be called when this project is executed first time
    params = __get_params(path)
    connection = pymysql.connect(host = params[0], user = params[1], password = params[2], port = params[3])
    cursor = connection.cursor()
    create_db_sql = "CREATE DATABASE {} DEFAULT CHARACTER SET utf8".format(DB_NAME)
    cursor.execute(create_db_sql)

    connection.select_db(DB_NAME)
    
    create_spot_table_sql = "CREATE TABLE IF NOT EXISTS Spot (cID VARCHAR(30)\
    NOT NULL, lecNum VARCHAR(30) NOT NULL, capacity INT(10) NOT NULL\
    ) CHARACTER SET=utf8"
    cursor.execute(create_spot_table_sql)

    create_wl_table_sql = "CREATE TABLE IF NOT EXISTS Waitlist (cID VARCHAR(30)\
    NOT NULL, lecNum VARCHAR(30) NOT NULL) CHARACTER SET=utf8"
    cursor.execute(create_wl_table_sql)

    print("database initialized")

    connection.close()

def get_connection(path, DB_NAME):
    params = __get_params(path)
    connection = pymysql.connect(host = params[0], user = params[1], password = params[2], port = params[3], db = DB_NAME)
    return connection

def commit_data(connection):
    try:
        connection.commit()
    except:
        connection.rollback()

def add_new_column(cursor, column_name):
    sql = "ALTER TABLE Spot ADD COLUMN {} INT(10) NOT NULL".format(column_name)
    cursor.execute(sql)
    sql2 = "ALTER TABLE Waitlist ADD COLUMN {} INT(10) NOT NULL".format(column_name)
    cursor.execute(sql2)

def update_spot_new_column(cursor, column_name, cID, lecNum, enrolment):
    sql = "UPDATE Spot SET {} = %s WHERE cID = %s and lecNum = %s".format(column_name)
    cursor.execute(sql, (enrolment, cID, lecNum))

def update_wl_new_column(cursor, column_name, cID, lecNum, waitlist):
    sql = "UPDATE Spot SET {} = %s WHERE cID = %s and lecNum = %s".format(column_name)
    cursor.execute(sql, (waitlist, cID, lecNum))

def init_spot(cursor, cID, lecNum, capacity):
    sql = "INSERT INTO Spot(cID, lecNum, capacity) values (%s, %s, %s)"
    cursor.execute(sql, (cID, lecNum, capacity))

def init_wl(cursor, cID, lecNum):
    sql = "INSERT INTO Waitlist(cID, lecNum) values (%s, %s)"
    cursor.execute(sql, (cID, lecNum))
