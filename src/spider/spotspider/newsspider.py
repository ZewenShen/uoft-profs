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
DB_PATH = '../../database.info'

BASE_URL = 'http://coursefinder.utoronto.ca/course-search/search/courseSearch/course/search?'
DETAIL_BASE_URL = 'http://coursefinder.utoronto.ca/course-search/search/courseInquiry?methodToCall=start&viewId=CourseDetails-InquiryView&courseId='

headers = {
    'Referer': 'http://coursefinder.utoronto.ca/course-search/search/courseSearch?viewId=CourseSearch-FormView&methodToCall=start',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

all_courses_params = {
    'queryText': '',
    'requirements': '',
    'campusParam': 'St. George'
}

COMMIT_BUFFER = 15

def get_all_courses_json():
    """
    Use the following url, you can get information of all the courses currently
    offered in json form at once.
    """
    url = BASE_URL + urlencode(all_courses_params)
    session = requests.session()
    try:
        session.get(url, headers=headers) # DON'T delete this line, otherwise you will get 403
        r = session.get(url, headers=headers) 
        if r.status_code == 200:
            return r.json()
        else:
            print('Error:', r.status_code)
    except requests.ConnectionError as e:
        print('Error', e.args)
        return None

def parse_json(json):
    """
    The json file contains all thousands of entries, each of them are one course.
    We enter the detailed page of each course, which contains the time
    arrangement, prof, etc of that course, and collect them first. Then we enter
    other information of this course into the directory.
    """
    for course in json['aaData']:
        detail_url = re.search("coursedetails/(.*?)'>", course[1]).group(1)
        url = DETAIL_BASE_URL + detail_url
        info_dict = parse_course_detail(get_course_detail(url))

        info_dict['cID'] = re.search(">(.*?)<", course[1]).group(1)
        """
        info_dict['cName'] = course[2]
        info_dict['credits'] = course[3]
        info_dict['campus'] = course[4].strip(' ')
        info_dict['department'] = course[5].strip(' ')
        """
        info_dict['term'] = course[6]
        """
        info_dict['division'] = course[7].strip(' ')
        """
        yield info_dict

def get_course_detail(url):
    """
    A trivial helper function which returns the static page of one course's
    detailed information, e.g., time arrangement, profs, etc.
    """
    try:
        r = requests.get(url, headers = headers)
        if r.status_code == 200:
            return r.text
        else:
            print('Error:', r.status_code)
    except requests.ConnectionError as e:
        print('Error: ', e.args)
        return None

def parse_course_detail(html):
    """
    Use beautifulsoup to get detailed information of one course, then put them
    in a dictionary.
    """
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('span', attrs = {'id': re.compile("^u2(45|54|63|72|81|90)_line\d.?$")})
    clean_pattern = re.compile(' \n|\n|\r')
    
    num_of_courses = len(table) // 6

    try:
        result = {
                "lecNum": ['-'.join(re.sub(clean_pattern, '', table[6 * i].getText()).upper().split()) for i in range(num_of_courses)],
                "size": [int(re.sub(clean_pattern, '', table[4 + 6 * i].getText())) for i in range(num_of_courses)],
                "currentEnrollment": [int(re.sub(clean_pattern, '', table[5 + 6 * i].getText())) for i in range(num_of_courses)]
                }
    except:
        result = {
                "lecNum": ['-'.join(re.sub(clean_pattern, '', table[6 * i].getText()).upper().split()) for i in range(num_of_courses)],
                "size": [int(re.sub(clean_pattern, '', table[4 + 6 * i].getText())) for i in range(num_of_courses)],
                "currentEnrollment": [0 for i in range(num_of_courses)]
                }
    return result

def add_new_column(column_name):
    connection = sdatabase.get_connection(DB_PATH, DB_NAME)
    with connection.cursor() as cursor:
        sdatabase.add_new_column(cursor, column_name)


def update_new_column(column_name):
    add_new_column(column_name)
    connection = sdatabase.get_connection(DB_PATH, DB_NAME)

    with connection.cursor() as cursor:
        Buffer = 0 
        count = 0
        for course_dict in parse_json(get_all_courses_json()):
            if "Summer" not in course_dict['term']:
                print(course_dict['cID'], course_dict['lecNum'])
                cID = course_dict['cID']
                lecNum = course_dict['lecNum']
                enrolment = course_dict['currentEnrollment']
                term = __transform_term(course_dict['term'])
                try:
                    for i in range(len(course_dict['lecNum'])):
                        sdatabase.new_update_spot_new_column(cursor, column_name, cID, lecNum[i], enrolment[i], term)
                except:
                    print("error when inserting {}".format(course_dict))
                    continue
                count += 1
                Buffer += 1
                if Buffer == COMMIT_BUFFER:
                    print("{}th time insert course data successfully".format(count))
                    sdatabase.commit_data(connection)
                    Buffer = 0

    sdatabase.commit_data(connection)
    connection.close()

def __transform_term(term):
    if '+' in term:
        return 'Y'
    elif 'Fall' in term:
        return 'F'
    else:
        return 'S'

if __name__ == '__main__':
    DB_PATH = '../../../database.info'
