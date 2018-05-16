import sys
sys.path.append("../spider/util")
import itertools
import pymysql
import Database
import time_conflicts_check

DB_NAME = "uoftcourses"
DB_PATH = "../../database.info"


def get_course_data(course_code, campus):
    """
    course_code: a string e.g. "CSC148"
    campus: a string - either "St. George", "Scarborough", or "Mississauga"
    Returns a list of tuples, with each tuple containing the data of a single section of the specified course
    """
    connection = Database.get_connection(DB_PATH, DB_NAME)
    cursor = connection.cursor()
    sql = "SELECT * FROM Course WHERE cID=%s AND campus=%s"
    cursor.execute(sql, (course_code, campus))

    return(list(cursor.fetchall()))

    
def get_all_possible_course_times(course_code, campus):
    """
    course_code: a string e.g. "CSC148"
    campus: a string - either "St. George", "Scarborough", or "Mississauga"
    Returns a tuple:
        - the first element is a list of strings containing all possible times (i.e. no conflicts) of combinations of lecture/tutorial/lab sections.
          For the format of the strings, see the process_times() function in the time_conflicts_check module
        - the second element is a list of lists of strings representing the respective lecture, tutorial and lab sections
        
    Note that the indices of the two lists correspond. For example, the first element of the first list has times that correspond
    to the class sections in the first element of the second list.
    """
    course_data = get_course_data(course_code, campus)
    
    lecture_times = []
    lecture_sections = []
    tutorial_times = []
    tutorial_sections = []
    lab_times = []
    lab_sections = []
    
    for course_data in all_course_data:
        if int(course_data[15]) >= int(course_data[14]):  # check if section is full
            continue
        lec_num = course_data[10]
        lec_comps = lec_num.split(" ")
        lec_time = course_data[11]
        
        if lec_comps[0] == "Lec": 
            lecture_times.append(lec_time)
            lecture_sections.append(lec_num)
        elif lec_comps[0] == "Tut": 
            tutorial_times.append(lec_time)
            tutorial_sections.append(lec_num)
        elif lec_comps[0] == "Pra": 
            lab_times.append(lec_time)
            lab_sections.append(lec_num)
        else:  # shouldn't happen
            raise ValueError
    
    all_times = list(itertools.product(lecture_times, tutorial_times, lab_times))  # all combinations of lecture/tutorial/lab
    all_section_combs = list(itertools.product(lecture_sections, tutorial_sections, lab_sections))
    all_possible_times = []
    all_possible_section_combs
    
    for i in range(len(all_times)):
        if (time_conflicts_check.no_time_conflict(all_times[i][0], all_times[i][1])  # check for internal time conflicts
                and time_conflicts_check.no_time_conflict(all_times[i][0], all_times[i][2])
                and time_conflicts_check.no_time_conflict(all_times[i][1], all_times[i][2])):
            all_possible_times.append(" ".join(all_times[i]))
            all_possible_section_combs.append(all_section_combs[i])
            
    return(all_possible_times, all_possible_section_combs)
    

def create_schedule_two_courses(times_course_1, sections_course_1, times_course_2, sections_course_2):
    """
    times_course_1: the first element of the output tuple of a get_all_possible_course_times() call on the first course
    sections_course_1: the second element of the output tuple of a get_all_possible_course_times() call on the first course
    times_course_2: the first element of the output tuple of a get_all_possible_course_times() call on the second course
    sections_course_2: the second element of the output tuple of a get_all_possible_course_times() call on the second course
    Returns a tuple identical in format to get_all_possible_course_times()
    
    The output times and sections will be all the schedules comprised of a combination of sections from the two courses
    with no time conflicts. If no such combinations exist, the return value is a tuple of two empty lists.
    """
    all_times = []
    all_sections = []
    
    for i in range(len(times_course_1)):
        for j in range(len(times_course_2)):
            if time_conflicts_check.no_time_conflict(times_course_1[i], times_course_2[j]):
                all_times.append(times_course_1[i] + " " times_course_2[j])
                all_sections.append(sections_course_1[i] + sections_course_2[j])
                
    return(all_times, all_sections)
        