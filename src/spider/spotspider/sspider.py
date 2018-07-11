import sys
sys.path.append('../../util/')
import Database
import json
import requests
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup

DB_NAME = 'uoftcourses'
DB_PATH = '../../database.info'

BASE_URL = 'https://timetable.iit.artsci.utoronto.ca/api/20189/courses?section={}'

headers = {
    'Referer': 'https://timetable.iit.artsci.utoronto.ca',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

COMMIT_BUFFER = 15


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




