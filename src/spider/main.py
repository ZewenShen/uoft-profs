import Database
import json
import requests
from urllib.parse import urlencode

BASE_URL = 'http://coursefinder.utoronto.ca/course-search/search/courseSearch/course/search?'

headers = {
    'Referer': 'http://coursefinder.utoronto.ca/course-search/search/courseSearch?viewId=CourseSearch-FormView&methodToCall=start',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

all_courses = 'queryText=&requirements=&campusParam=St.%20George,Scarborough,Mississaga'

all_courses_params = {
    'queryText': '',
    'requirements': '',
    'campusParam': 'St. George,Scarborough,Mississaga'
}

def get_all_courses():
    url = BASE_URL + urlencode(all_courses_params)
    session = requests.session()
    try:
        session.get(url, headers=headers) # don't delete this line. It enables you to get cookies, otherwise you will get 403
        r = session.get(url, headers=headers) 
        if r.status_code == 200:
            return r.json()
    except requests.ConnectionError as e:
        print('Error', e.args)
        return None


def get_courses(deptId, divId):
    params = {
        'deptId': deptId + ' ',
        'divId': divId
    }

    url = BASE_URL + urlencode(params)

    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.json()
    except requests.ConnectionError as e:
        print('Error', e.args)
        return None
