import selection_utils
import sys
sys.path.append("../util")
import Database
import itertools

PATH = '../../database.info'
DB_NAME = 'uoftcourses'

def get_courses_arrangement_for_multiple_courses(cursor, cID_list, term):
    separate_arrangement = get_courses_arrangement_for_separate_course(cursor, cID_list, term)
    result = []
    for possible_schedule in itertools.product(*separate_arrangement):
        if not has_conflict(possible_schedule):
            result.append(possible_schedule)
    return result

def filter_arrangement_result(arrangement_result):
    filtered_result = []
    for possible_schedule in arrangement_result:
        temp_result = []
        for course in possible_schedule:
            for lec_info in course:
                temp_result.append([lec_info[0], lec_info[1]])
        filtered_result.append(temp_result)
    return filtered_result


def has_conflict(possible_schedule):
    schedule = {"MONDAY": [False for i in range(48)],
                "TUESDAY": [False for i in range(48)],
                "WEDNESDAY": [False for i in range(48)],
                "THURSDAY": [False for i in range(48)],
                "FRIDAY": [False for i in range(48)]
                }
    for course in possible_schedule:
        for lec_info in course:
            lec_info_day = lec_info[selection_utils.TIME_INDEX]
            for day in selection_utils.DAY:
                for time_tuple in lec_info_day[day]:
                    for i in range(time_tuple[0], time_tuple[1]):
                        if schedule[day][i] is True:
                            return True
                        else:
                            schedule[day][i] = True
    return False

def get_courses_arrangement_for_separate_course(cursor, cID_list, term):
    courses_info = _get_processed_multiple_courses_data(cursor, cID_list, term)
    comb = _get_combination_of_multiple_courses(courses_info)
    return comb

def _get_processed_multiple_courses_data(cursor, cID_list, term):
    """
    Take a list of cIDs, then return the data of them. 
    """
    result = []
    for cID in cID_list:
        processed_data = selection_utils.get_processed_course_data(cursor, cID, term)
        result.append(processed_data)
    return result

def _get_combination_of_multiple_courses(courses_info):
    """
    Take a list of cIDs' data, return all the possible combination of separate
    course.
    """
    result = []
    for course_info in courses_info:
        comb = selection_utils.get_combination_of_one_course(course_info)
        selection_utils._filter_combination(comb)
        result.append(comb)
    return result

