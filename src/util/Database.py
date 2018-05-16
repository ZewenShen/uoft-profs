import pymysql

def __get_params(path):
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

    create_course_table_sql = "CREATE TABLE IF NOT EXISTS Course (cID VARCHAR(30) NOT NULL, cName\
    VARCHAR(300) NOT NULL, credits FLOAT NOT NULL, campus VARCHAR(150) NOT NULL,\
    department VARCHAR(160) NOT NULL, term VARCHAR(150) NOT NULL, division\
    VARCHAR(200) NOT NULL, prerequisites VARCHAR(1000), exclusion VARCHAR(1000), br\
    VARCHAR(200), lecNum VARCHAR(30) NOT NULL, lecTime VARCHAR(125) NOT\
    NULL, instructor VARCHAR(500), location VARCHAR(250), size INT(5),\
    currentEnrollment INT(5), PRIMARY KEY (cID, term, lecNum))"
    cursor.execute(create_course_table_sql)

    create_eval_table_sql = "CREATE TABLE IF NOT EXISTS Eval (department\
    VARCHAR(160) NOT NULL, cID VARCHAR(30) NOT NULL, cName VARCHAR(300) NOT\
    NULL, lecNum VARCHAR(30) NOT NULL, campus VARCHAR(150) NOT NULL, term\
    VARCHAR(150) NOT NULL, instructor VARCHAR(150), instructorFullName\
    VARCHAR(200), intellectuallySimulating FLOAT(10), deeperUnderstanding\
    FLOAT(10), courseAtmosphere FLOAT(10), homeworkQuality FLOAT(10),\
    homeworkFairness FLOAT(10), overallQuality FLOAT(10), enthusiasm FLOAT(10),\
    workload FLOAT(10), recommend FLOAT(10), numInvited INT(10), numResponded\
    INT(10), PRIMARY KEY (cID, term, lecNum, instructorFullName))"
    cursor.execute(create_eval_table_sql)

    print("database intialized")

    connection.close()


def get_connection(path, DB_NAME):
    params = __get_params(path)
    connection = pymysql.connect(host = params[0], user = params[1], password = params[2], port = params[3], db = DB_NAME)
    return connection


def insert_course_data(cursor, info_dict):
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
    lecNum_list = info_dict['lecNum']
    lecTime_list = info_dict['lecTime']
    instructor_list = info_dict['instructor']
    location_list = info_dict['location']
    size_list = info_dict['size']
    currentEnrollment_list = info_dict['currentEnrollment']

    num_of_courses = len(lecNum_list) # this must be equal to len(info_dict['lecTime'], etc.

    for i in range(num_of_courses):
        print(cID)
        cursor.execute(sql, (cID, cName, credits, campus, department, term,\
            division, prerequisites, exclusion, br, lecNum_list[i], lecTime_list[i],\
            instructor_list[i], location_list[i], size_list[i], currentEnrollment_list[i]))

def insert_eval_data(cursor, info_dict):
    sql = "INSERT INTO Eval (department, cID, cName, lecNum, campus, term,\
        instructor, instructorFullName, intellectuallySimulating,\
        deeperUnderstanding, courseAtmosphere, homeworkQuality,\
        homeworkFairness, overallQuality, enthusiasm, workload, recommend,\
        numInvited, numResponded) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,\
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    info_dict = {k: (lambda x: None if x == 'N/A' else x)(v) for k, v in info_dict.items()} 
    # clean data in info_dict (since N/A may appear, which can't be recognized by sql.)

    department = info_dict['department']
    cID = info_dict['cID']
    cName = info_dict['cName']
    lecNum = info_dict['lecNum']
    campus = info_dict['campus']
    term = info_dict['term']
    instructor = info_dict['instructor']
    instructorFullName = info_dict['instructorFullName']
    intellectuallySimulating = info_dict['intellectuallySimulating']
    deeperUnderstanding = info_dict['deeperUnderstanding']
    courseAtmosphere = info_dict['courseAtmosphere']
    homeworkQuality = info_dict['homeworkQuality']
    homeworkFairness = info_dict['homeworkFairness']
    overallQuality = info_dict['overallQuality']
    enthusiasm = info_dict['enthusiasm']
    workload = info_dict['workload']
    recommend = info_dict['recommend']
    numInvited = info_dict['numInvited']
    numResponded = info_dict['numResponded']

    print(cID)
    cursor.execute(sql, (department, cID, cName, lecNum, campus, term,\
        instructor, instructorFullName, intellectuallySimulating,\
        deeperUnderstanding, courseAtmosphere, homeworkQuality,\
        homeworkFairness, overallQuality, enthusiasm, workload, recommend,\
        numInvited, numResponded))



def commit_data(connection):
    try:
        connection.commit()
    except:
        connection.rollback()

def get_course_data_by_cID_and_campus(cursor, cID, campus):
    """
    cursor: the cursor of our connection.
    course_code: a string, e.g., "CSC148"
    campus: a string - either "St. George", "Scarborough", or "Mississauga"
    -------------------------------------------------------
    Returns a list of tuples, with each tuple containing the data of a single
    section of the specified course
    -------------------------------------------------------
    We use cursor here to avoid unnecessary connections with database.
    """
    sql = "SELECT * FROM Course Where cID like %s And campus = %s"
    cursor.execute(sql, ("%{}%".format(cID), campus))

    return list(cursor.fetchall())
