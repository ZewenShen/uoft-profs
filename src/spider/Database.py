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
    VARCHAR(50) NOT NULL, prerequisites VARCHAR(50), exclusion VARCHAR(40), br\
    VARCHAR(50), lecNum VARCHAR(20) NOT NULL, lecTime VARCHAR(125) NOT\
    NULL, instructor VARCHAR(80), location VARCHAR(60), size INT(5),\
    currentEnrollment INT(5), PRIMARY KEY (cID, term, lecNum))"
    cursor.execute(sql)

    db.close()


def get_connection(path):
    params = get_params(path)
    connection = pymysql.connect(host = params[0], user = params[1], password = params[2], port = params[3], db = DB_NAME)
    return connection


def insert_data(cursor, info_dict):
    sql = "INSERT INTO Course(cID, cName, credits, campus, department, term,\
    division, prerequisites, exclusion, br, lecNum, lecTime, instructor,\
    location, size, currentEnrollment) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    cID = info_dict['cID']
    cName = info_dict['cName']
    credits = info_dict['credits']
    campus = info_dict['campus']
    department = info_dict['department']
    term = info_dict['term']
    division = info_dict['division']
    prerequisites = info_dict['prerequisites']
    exclusion = info_dict['exclusion']
    br = info_dict['br']

    num_of_courses = len(info_dict['lecNum']) # this must be equal to len(info_dict['lecTime'], etc.

    for i in range(num_of_courses):
        cursor.execute(sql, (cID, cName, credits, campus, department, term,\
            division, prerequisites, exclusion, br, lecNum[i], lecTime[i],\
            instructor[i], location[i], size[i], currentEnrollment[i]))


def commit_data(connection):
    try:
        connection.commit()
    except:
        connection.rollback()

