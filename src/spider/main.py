import Database
import json
import requests
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup

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
    'campusParam': 'St. George,Scarborough,Mississaga'
}

def get_all_courses_json():
    url = BASE_URL + urlencode(all_courses_params)
    session = requests.session()
    try:
        session.get(url, headers=headers) # DON'T delete this line, otherwise you will get 403
        r = session.get(url, headers=headers) 
        if r.status_code == 200:
            return r.json()
    except requests.ConnectionError as e:
        print('Error', e.args)
        return None

def parse_json(json):
    for page in json['aaData']:
        for course in page:
            detail_url = re.search(".*?coursedetails/(.*?)'>", course[1]).group(1)
            url = DETAIL_BASE_URL + detail_url
            detail_dict = parse_course_detail(get_course_detail(url))
            


def get_course_detail(url):
    try:
        r = requests.get(url, headers = headers)
        if r.status_code == 200:
            return parse_course_detail(r.text)
    except requests.ConnectionError as e:
        print('Error', e.args)
        return None

def parse_course_detail(html):
    soup = BeautifulSoup(html, 'lxml')
    taglist = soup.find_all('span', attrs = {'id': re.compile("^u2(45|54|63|72|81|90)_line\d$")})
    clean_pattern = re.compile(' \n|\n|\r')
    return {
            "Lec_Num": [re.sub(clean_pattern, '', taglist[6 * i].getText()) for i in range(len(taglist) // 6)],
            "Lec_Time": [re.sub(clean_pattern, '', taglist[1 + 6 * i].getText()) for i in range(len(taglist) // 6)],
            "Instructor": [re.sub(clean_pattern, '', taglist[2 + 6 * i].getText()) for i in range(len(taglist) // 6)],
            "Location": [re.sub(clean_pattern, '', taglist[3 + 6 * i].getText()) for i in range(len(taglist) // 6)],
            "Size": [re.sub(clean_pattern, '', taglist[4 + 6 * i].getText()) for i in range(len(taglist) // 6)],
            "Current_Enrollment": [re.sub(clean_pattern, '', taglist[5 + 6 * i].getText()) for i in range(len(taglist) // 6)]
            }



