"""
Use the no_time_conflict() function detailed below to check for a time conflict between courses.

This file is mainly written by James Jiang. I only modified it a little bit.
"""
import sys
sys.path.append("../util")
import Database
import itertools

PATH = "../../database.info"
DB_NAME = "uoftcourses"
DAY = ("MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY")
LEC_NUM_INDEX = 1
TIME_INDEX = 2

def get_and_filter_course_data(cursor, cID, term):
    data_processed = get_processed_course_data(cursor, cID, term)
    comb = get_combination_of_one_course(data_processed)
    _filter_combination(comb)
    return comb

def __get_course_data(cursor, cID, term):
    """
    >>> __get_course_data(cursor, "CSC148H1", "Fall")
    [['CSC148H1', 'Lec 0101', 'TUESDAY 10:00-12:00 FRIDAY 10:00-11:00'],
     ['CSC148H1', 'Lec 0102', 'TUESDAY 10:00-12:00 FRIDAY 10:00-11:00'],
     ['CSC148H1', 'Tut 0101', 'THURSDAY 09:00-11:00'], 
     ['CSC148H1', 'Tut 0201', 'THURSDAY 11:00-13:00'], 
     ['CSC148H1', 'Tut 0301', 'THURSDAY 13:00-15:00'], 
     ['CSC148H1', 'Tut 5101', 'THURSDAY 19:00-21:00']]
    """
    sql = "SELECT cID, lecNum, lecTime from Course where cID like %s and term like %s"
    if cID[-2] == 'Y':
        term = 'Fall'
    cursor.execute(sql, (cID, "%{}%".format(term)))
    return list(map(list, list(cursor.fetchall())))

def _process_raw_course_data(raw_course_data_list):
    """
    Let the string form of the course time to be dictionary form. 
    """
    for item in raw_course_data_list:
        item[2] = process_times(item[2])

def get_processed_course_data(cursor, cID, term):
    result = __get_course_data(cursor, cID, term)
    _process_raw_course_data(result)
    return result

def get_combination_of_one_course(course_info):
    lec_list = [item for item in course_info if 'Lec' in item[LEC_NUM_INDEX]]
    tut_list = [item for item in course_info if 'Tut' in item[LEC_NUM_INDEX]]
    pra_list = [item for item in course_info if 'Pra' in item[LEC_NUM_INDEX]]
    
    if lec_list != []:
        comb = lec_list
        if list(itertools.product(comb, tut_list)) != []:
            comb = list(itertools.product(comb, tut_list))
            if list(itertools.product(comb, pra_list)) != []:
                comb = list(itertools.product(comb, pra_list))
        elif list(itertools.product(comb, pra_list)) != []:
            comb = list(itertools.product(comb, pra_list))
        else:
            comb = [[item] for item in lec_list]
    elif tut_list != []:
        comb = tut_list
        if list(itertools.product(comb, pra_list)) != []:
            comb = list(itertools.product(comb, pra_list))
        else:
            comb = [[item] for item in tut_list]
    else:
        comb = [[item] for item in pra_list]
        
    return comb

def _filter_combination(comb):
    for separated_schedule in comb:
        if len(separated_schedule) != 1 and _is_not_valid(separated_schedule):
            comb.remove(separated_schedule)

def _is_not_valid(separated_schedule):
    """
    Return false if the combination we get conflicts.
    """
    schedule = {"MONDAY": [False for i in range(48)],
                "TUESDAY": [False for i in range(48)],
                "WEDNESDAY": [False for i in range(48)],
                "THURSDAY": [False for i in range(48)],
                "FRIDAY": [False for i in range(48)]
                }
    for item in separated_schedule:
        item_day = item[TIME_INDEX]
        for day in DAY: # 5 times
            for time_tuple in item_day[day]: # 0~2 times basically
                for i in range(time_tuple[0], time_tuple[1]):
                    if schedule[day][i] is True:
                        return True
                    else:
                        schedule[day][i] = True
    return False


def time_to_num(time):
    """
    time: a string representing a time, with hour and minute separated by a colon (:)
    Returns a number

    e.g. time_to_num("9:00") -> 9 * 2 = 18
         time_to_num("21:00") -> 21 * 2 = 42
         time_to_num("12:30") -> 12.5 * 2 = 25
    """
    time_comps = time.split(":")

    assert len(time_comps) == 2;
    assert int(time_comps[1]) == 0 or int(time_comps[1]) == 30

    result = int(time_comps[0])*2
    return result if int(time_comps[1]) == 0 else result + 1

def num_to_time(num):
    """
    Turn the num returned from method "time_to_num" back to the string form.

    e.g. num_to_time(18) -> "9:00"
         num_to_time(25) -> "12:30"
    """
    return str(num//2) + ':00' if num % 2 == 0 else str(num//2) + ':30' 

def process_times(times):
    """
    times: a string of weekdays and time-slots of courses, delimited by spaces
    Returns a list of tuples containing the weekday, start time, and duration of the courses
    >>> process_times("WEDNESDAY 18:00-21:00")
    {'WEDNESDAY': [(36, 42)], 'FRIDAY': [], 'TUESDAY': [], 'MONDAY': [], 'THURSDAY':
        []}
    e.g. process_times("MONDAY 18:00-20:00 THURSDAY 18:00-21:00") -> [("MONDAY", 18, 2), ("THURSDAY", 18, 3)]
         process_times("WEDNESDAY 13:30-15:00") -> [("WEDNESDAY", 13.5, 1.5)]

    IMPORTANT: this function assumes that the input string is in a format similar to the examples above
    """
    all_times = {"MONDAY": [],
                 "TUESDAY": [],
                 "WEDNESDAY": [],
                 "THURSDAY": [],
                 "FRIDAY": []}
    times_comps = times.split(" ")
    assert len(times_comps) % 2 == 0

    for i in range(0, len(times_comps), 2):
        assert times_comps[i] in all_times

        start_end = times_comps[i + 1].split("-")
        day = times_comps[i]

        start = time_to_num(start_end[0])
        end = time_to_num(start_end[1])

        all_times[day].append((start, end))

    return all_times

