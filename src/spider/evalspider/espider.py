import sys
sys.path.append('../../util/')
import Database
import json
import requests
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from xml.etree.ElementTree import fromstring
from functools import reduce

DB_NAME = 'uoftcourses'
DB_PATH = '../../database.info'
PAGE_SIZE = 50
LEC_NUM_LENGTH = 4
TOTAL_EVAL_DATA = 18075
COMMIT_BUFFER = 15

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
    """
    pageActuelle: int 
    Represents the number of page you want to scrape.
    ----------------------------------------------
    This method will return a string which is in xml form, comprising all the
    eval information.
    """
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
    """
    xml_string: str 
    A string in xml form comprising lots of course eval information.
    --------------------------------------------------------------------
    Use helper function "extract_eval_data" to clean courses eval data one by one.
    """
    tree = fromstring(xml_string) # turn the xmlstring into real xml structure
    eval_data_in_xml = tree[0] # the eval data we need is in index 0
    soup = BeautifulSoup(eval_data_in_xml.text, 'lxml')
    
    tr_taglist = soup.find_all('tr', attrs={'class': 'gData'})
    
    cleaned_eval_data_list = []
    for tr_tag in tr_taglist:
        data = extract_eval_data(tr_tag)
        if data is not None:
            cleaned_eval_data_list.append(data)
    
    return cleaned_eval_data_list

def extract_eval_data(tr_tag):
    """
    For further information, please read the codes & comments. It's clear.
    """
    td_taglist = tr_tag.find_all('td')

    uncleaned_course_info = td_taglist[1].getText() # e.g., 'Human Embroyology ANA301H1-S-LEC0101'
    try:
        __search_result = re.search(' -?([A-Z0-9]+? ?-(\w ?-)? ?[^\s]*) ?', uncleaned_course_info)
        uncleaned_courseID = __search_result.group(1) # e.g., "ANA201H1-S-LEC0101"
        lecNum = "Lec " + uncleaned_courseID[len(uncleaned_courseID) - LEC_NUM_LENGTH:] # use 'Lec' instead of 'LEC' here to sync with Course database table
        cID = uncleaned_courseID.split('-')[0]
        season = uncleaned_courseID.split('-')[1] if len(uncleaned_courseID.split('-')) == 3 else ''
        cName = uncleaned_course_info[: __search_result.span()[0]]
    except AttributeError as e:
        print("Error when extracting eval data from {}:".format(uncleaned_course_info), e.args)
        return None

    return {
        "department": td_taglist[0].getText(),
        "cID": cID,
        "cName": cName,
        "lecNum": lecNum, 
        "campus": "St. George",
        "term": "{} {} {}".format(td_taglist[5].getText(), td_taglist[4].getText(), season) if season != '' else "{} {}".format(td_taglist[5].getText(), td_taglist[4].getText()),
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

def main():
    connection = Database.get_connection(DB_PATH, DB_NAME)
    cursor = connection.cursor()

    Buffer = 0
    count = 0
    for i in range(1, TOTAL_EVAL_DATA // PAGE_SIZE + 1):
        for row in clean_course_evals(get_course_evals(i)):
            Database.insert_eval_data(cursor, row)
            count += 1
            Buffer += 1
            if Buffer == COMMIT_BUFFER:
                print("{}th time insert eval data successfully".format(count))
                Database.commit_data(connection)
                Buffer = 0
    Database.commit_data(connection)
    connection.close()

if __name__ == '__main__':
    DB_PATH = '../../../database.info' # this should be changed only when "python3
    # espider.py" is called. In the case that espider.main() is called by other
    # file, the DBpath shouldn't be changed
    main()
