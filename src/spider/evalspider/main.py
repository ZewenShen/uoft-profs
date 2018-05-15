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
    tree = fromstring(xml_string) # turn the xmlstring into real xml structure
    eval_data_in_xml = tree[0] # the eval data we need is in index 0
    soup = BeautifulSoup(eval_data_in_xml.text, 'lxml')
    
    tr_taglist = soup.find_all('tr', attrs={'class': 'gData'})
    taglist = soup.find_all('td')

    uncleaned_course_info = taglist[1].getText() # e.g., 'Human Embroyology ANA301H1-SLEC0101'
    __split_index = uncleaned_course_info.rfind(' ') + 1
    uncleaned_courseID = uncleaned_course_info[__split_index:] # e.g., "ANA201H1-S-LEC0101"
    lecNum = "Lec " + re.search("-LEC(\d{4})$", uncleaned_courseID).group(1) # use 'Lec' instead of 'LEC' here to sync with Course database table
    cID = uncleaned_courseID.split('-')[0]
    season = uncleaned_courseID.split('-')[1]
    cName = uncleaned_course_info[: __split_index]

    return {
        "department": taglist[0].getText(),
        "cID": cID,
        "cName": cName,
        "lecNum": lecNum, 
        "campus": "St. George",
        "term": "{} {} {}".format(taglist[5].getText(), taglist[4].getText(), season),
        "instructor": "{} {}".format(taglist[3].getText()[0], taglist[2].getText()), # the instructor column in Course database table only have initial first name instead of full name
        "instructorFullName": "{} {}".format(taglist[3].getText(), taglist[2].getText()),
        "intellectuallySimulating": taglist[6].getText(),
        "deeperUnderstanding": taglist[7].getText(),
        "courseAtmosphere": taglist[8].getText(),
        "homeworkQuality": taglist[9].getText(),
        "homeworkFairness": taglist[10].getText(),
        "overallQuality": taglist[11].getText(),
        "enthusiasm": taglist[12].getText(),
        "workload": taglist[13].getText(),
        "recommend": taglist[14].getText(),
        "numInvited": taglist[15].getText(),
        "numResponded": taglist[16].getText()
    }


def extract_one_course(tr_taglist):
    td_taglist = tr_taglist.find_all('td')

    uncleaned_course_info = td_taglist[1].getText() # e.g., 'Human Embroyology ANA301H1-SLEC0101'
    __split_index = uncleaned_course_info.rfind(' ') + 1
    uncleaned_courseID = uncleaned_course_info[__split_index:] # e.g., "ANA201H1-S-LEC0101"
    lecNum = "Lec " + re.search("-LEC(\d{4})$", uncleaned_courseID).group(1) # use 'Lec' instead of 'LEC' here to sync with Course database table
    cID = uncleaned_courseID.split('-')[0]
    season = uncleaned_courseID.split('-')[1]
    cName = uncleaned_course_info[: __split_index]

    return {
        "department": taglist[0].getText(),
        "cID": cID,
        "cName": cName,
        "lecNum": lecNum, 
        "campus": "St. George",
        "term": "{} {} {}".format(td_taglist[5].getText(), td_taglist[4].getText(), season),
        "instructor": "{} {}".format(td_taglist[3].getText()[0], td_taglist[2].getText()), # the instructor column in Course database table only have initial first name instead of full name
        "instructorFullName": "{} {}".format(td_taglist[3].getText(), td_taglist[2].getText()),
        "intellectuallySimulating": td_taglist[6].getText(),
        "deeperUnderstanding": td_taglist[7].getText(),
        "courseAtmosphere": td_taglist[8].getText(),
        "homeworkQuality": td_taglist[9].getText(),
        "homeworkFairness": td_taglist[10].getText(),
        "overallQuality": td_taglist[11].getText(),
        "enthusiasm": td_taglist[12].getText(),
        "workload": td_taglist[13].getText(),
        "recommend": td_taglist[14].getText(),
        "numInvited": td_taglist[15].getText(),
        "numResponded": td_taglist[16].getText()
    }

