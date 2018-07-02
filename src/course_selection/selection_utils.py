"""
Use the no_time_conflict() function detailed below to check for a time conflict between courses.

This file is mainly written by James Jiang. I only modified it a little bit.
"""
import sys
sys.path.append("../util")
import Database

PATH = "../../database.info"
DB_NAME = "uoftcourses"

def __get_course_data(cursor, cID, campus, term):
    """
    >>> get_course_data(cursor, "CSC148", "St. George", "Fall")
    [['csc148h1', 'lec 0101', 'tuesday 10:00-12:00 friday 10:00-11:00'],
    ['csc148h1', 'lec 0102', 'tuesday 10:00-12:00 friday 10:00-11:00'],
    ['csc148h1', 'tut 0101', 'thursday 09:00-11:00'], ['csc148h1', 'tut 0201',
    'thursday 11:00-13:00'], ['csc148h1', 'tut 0301', 'thursday 13:00-15:00'],
    ['csc148h1', 'tut 5101', 'thursday 19:00-21:00']]
    """
    sql = "SELECT cID, lecNum, lecTime from Course where cID like %s and campus = %s and term like %s"
    cursor.execute(sql, ("{}%".format(cID), campus, "%{}%".format(term)))
    return list(map(list, list(cursor.fetchall())))

def _process_raw_course_data(raw_course_data_list):
    """
    Let the string form of the course time to be dictionary form. 
    """
    for item in raw_course_data_list:
        item[2] = process_times(item[2])

def get_course_data(cursor, cID, campus, term):
    result = __get_course_data(cursor, cID, campus, term)
    _process_raw_course_data(result)
    return result

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


def no_time_conflict(times, times_to_check):
    """
    times: a string parameter to process_times()
    times_to_check: a string parameter to process_times()
    Returns True if times_to_check and times has no time conflict; False otherwise

    e.g. no_time_conflict("MONDAY 18:00-20:00 THURSDAY 18:00-21:00", "MONDAY 17:00-19:00") -> False
         no_time_conflict("MONDAY 18:00-20:00 THURSDAY 18:00-21:00", "MONDAY 17:00-18:00") -> True
         no_time_conflict("MONDAY 18:00-20:00", "TUESDAY 18:00-20:00") -> True
         no_time_conflict("MONDAY 12:00-14:00 MONDAY 12:00-13:00", "TUESDAY 9:00-10:00") -> True

    IMPORTANT: this function assumes that the input parameters are in a format given in process_times()
    In addition, this function assumes that each set of times does not have a conflict with itself
    """
    times_ = process_times(times)
    times_to_check_ = process_times(times_to_check)

    for time in times_:
        weekday = time[0]
        for time_to_check in times_to_check_:
            if time_to_check[0] == weekday:
                if ((time_to_check[1] >= time[1] and time_to_check[1] < (time[1] + time[2]))
                        or (time[1] >= time_to_check[1] and time[1] < (time_to_check[1] + time_to_check[2]))):
                            return False
    return True
