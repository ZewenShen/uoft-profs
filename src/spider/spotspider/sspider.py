import sys
sys.path.append('../../util/')
import Database
import json
import requests
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import sdatabase

DB_NAME = 'uoftspots'
DB_PATH = '../../../database.info'

BASE_URL = 'https://timetable.iit.artsci.utoronto.ca/api/20189/courses?section={}'

headers = {
    'Referer': 'https://timetable.iit.artsci.utoronto.ca',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

COMMIT_BUFFER = 15

SEMESTERS = ['F', 'S', 'Y']


def get_json_of_course_list(semester):
    """
    Semester can be "F", "S" or "Y"
    """
    r = requests.get(BASE_URL.format(semester), headers=headers)
    return r.json()

def process_json(json):
    for course_name in json:
        course = json[course_name]
        for session_name in course['meetings']:
            session_info = course['meetings'][session_name]
            try:
                result = {
                        'cID': course_name,
                        'session': session_name,
                        'enrollmentCapacity': session_info['enrollmentCapacity'],
                        'actualEnrolment': session_info['actualEnrolment'],
                        'actualWaitlist': session_info['actualWaitlist']
                        }
            except KeyError:
                print("Error when processing the json of {}".format(course_name))
            yield result

def init_db(path, DB_NAME):
    sdatabase.init_db(path, DB_NAME)
    connection = sdatabase.get_connection(DB_PATH, DB_NAME)

    commit_count = 0

    with connection.cursor() as cursor:
        for semester in SEMESTERS:
            for item in process_json(get_json_of_course_list(semester)):
                cID = item['cID']
                lecNum = item['session']
                print(cID, lecNum)
                capacity = item['enrollmentCapacity']
                sdatabase.init_spot(cursor, cID, lecNum, capacity)
                sdatabase.init_wl(cursor, cID, lecNum)

                commit_count += 1
                if commit_count >= COMMIT_BUFFER:
                    commit_count = 0
                    sdatabase.commit_data(connection)
    sdatabase.commit_data(connection)
    connection.close()
    
def update_new_column(column_name):
    add_new_column(column_name)

    connection = sdatabase.get_connection(DB_PATH, DB_NAME)

    commit_count = 0
    with connection.cursor() as cursor:
        for semester in SEMESTERS:
            for item in process_json(get_json_of_course_list(semester)):
                cID = item['cID']
                lecNum = item['session']
                print(cID, lecNum)
                enrolment = item['actualEnrolment']
                waitlist = item['actualWaitlist']

                sdatabase.update_spot_new_column(cursor, column_name, cID, lecNum, enrolment)
                sdatabase.update_wl_new_column(cursor, column_name, cID, lecNum, waitlist)

                commit_count += 1
                if commit_count >= COMMIT_BUFFER:
                    commit_count = 0
                    sdatabase.commit_data(connection)
    sdatabase.commit_data(connection)
    connection.close()

def add_new_column(column_name):
    connection = sdatabase.get_connection(DB_PATH, DB_NAME)
    with connection.cursor() as cursor:
        sdatabase.add_new_column(cursor, column_name)
