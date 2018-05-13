import pymysql

DB_NAME = 'uoft-courses'

def get_params(path):
    f = open(path, 'r')
    params = f.readlines()
    f.close()
    params = [item.strip('\n') for item in params]
    params[3] = int(params[3])
    return params 


def init_db(path): # Should be called when this project is executed first time
    params = get_params(path)
    connection = pymysql.connect(host = params[0], user = params[1], password = params[2], port = params[3])
    cursor = connection.cursor()
    sql = "CREATE DATABASE {} DEFAULT CHARACTER SET utf8".format(DB_NAME)
    cursor.execute(sql)

    connection.select_db(DB_NAME)
    cursor = connection.cursor()
    sql = "CREATE TABLE IF NOT EXISTS Course (cID VARCHAR(10) NOT NULL, cName\
    VARCHAR(75) NOT NULL, credits FLOAT NOT NULL, campus VARCHAR(50) NOT NULL,\
    department VARCHAR(50) NOT NULL, term VARCHAR(25) NOT NULL, division\
    VARCHAR(50) NOT NULL, lecNum VARCHAR(20) NOT NULL, lecTime VARCHAR(125) NOT\
    NULL, instructor VARCHAR(80), location VARCHAR(60), size INT(5),\
    currentEnrollment INT(5))"
    cursor.execute(sql)

    db.close()


def get_connection(path):
    params = get_params(path)
    connection = pymysql.connect(host = params[0], user = params[1], password = params[2], port = params[3], db = DB_NAME)
    return connection


def insert_data(cursor):
    pass 
