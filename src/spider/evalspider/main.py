import sys
sys.path.append('../util/')
import Database
import json
import requests
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from xml.etree.ElementTree import fromstring

DB_NAME = 'uoftevals'
DB_PATH = '../../../database.info'
PAGE_SIZE = 1

BASE_URL = 'https://course-evals.utoronto.ca/BPI/fbview-WebService.asmx/getFbvGrid'

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://course-evals.utoronto.ca',
    'Referer': 'https://course-evals.utoronto.ca/BPI/fbview.aspx?blockid=seipDRPeug8Eu',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
}

payload = {
    "strUiCultureIn": "en-US",
    "datasourceId": "7160",
    "blockId": "900",
    "subjectColId": "1",
    "subjectValue": "____[-1]____",
    "detailValue": "____[-1]____",
    "gridId": "fbvGrid",
    "pageActuelle": None, #To make data clean easy, we get 1 course every time
    "strOrderBy": ["col_1", "asc"],
    "strFilter": ["", "", "ddlFbvColumnSelectorLvl1", ""],
    "sortCallbackFunc": "__getFbvGrid",
    "userid": "",
    "pageSize": "{}".format(PAGE_SIZE)
}

def get_course_evals(pageActuelle):
    payload["pageActuelle"] = pageActuelle
    
    try:
        r = requests.post(BASE_URL, data=payload, headers=headers)
        if r.status_code == 200:
            return r.text
        else:
            print('Error', r.status_code)
    except requests.ConnectionError as e:
        print('Error', e.args)

def clean_course_evals(xml_string):
    tree = fromstring(xml_string)
    eval_data_in_xml = tree[0]
    soup = BeautifulSoup(eval_data_in_xml.text, 'lxml')
    
    taglist = soup.find_all('td')

    clean_pattern = re.compile('<td.*?>|</td>')

    lecNum = "Lec " + re.search("-LEC(\d{4})$", taglist[1].getText()).group(1)

    return {
        "department": taglist[0].getText(),
        #"cID": ,
        "lecNum": lecNum, 
        "campus": "St. George",
        "instructor": "{} {}".format(taglist[3], taglist[2]),
        "enthusiasm": taglist[12].getText(),
        "workload": taglist[13].getText(),
        "recommend": taglist[14].getText(),
        "numInvited": taglist[15].getText(),
        "numResponded": taglist[16].getText()
    }





