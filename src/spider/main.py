import ConnectDatabase
import json
import requests
from urllib.parse import urlencode

BASE_URL = 'http://coursefinder.utoronto.ca/course-search/search/courseSearch/course/browseSearch?'

headers = {
    'Referer': 'http://coursefinder.utoronto.ca/course-search/search/courseSearch/course/browseSearch?viewId=CourseSearch-FormView&methodToCall=start',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

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
