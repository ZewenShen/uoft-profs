"""
Use the no_time_conflict() function detailed below to check for a time conflict between courses.
"""


def time_to_num(time):
    """
    time: a string representing a time, with hour and minute separated by a colon (:)
    Returns a number

    e.g. time_to_num(9:00) -> 9
         time_to_num(21:00) -> 21
         time_to_num(12:30) -> 12.5
    """
    time_comps = time.split(":")
    if int(time_comps[1]) == 0:
        return int(time_comps[0])
    return(int(time_comps[0]) + int(time_comps[1])/60)


def process_times(times):
    """
    times: a string of weekdays and time-slots of courses, delimited by spaces
    Returns a list of tuples containing the weekday, start time, and duration of the courses

    e.g. process_times("MONDAY 18:00-20:00 THURSDAY 18:00-21:00") -> [("MONDAY", 18, 2), ("THURSDAY", 18, 3)]
         process_times("WEDNESDAY 13:30-15:00") -> [("WEDNESDAY", 13.5, 1.5)]

    IMPORTANT: this function assumes that the input string is in a format similar to the examples above
    """
    all_times = []
    times_comps = times.split(" ")

    for i in range(0, len(times_comps), 2):
        start_end = times_comps[i + 1].split("-")
        start = time_to_num(start_end[0])
        dur = time_to_num(start_end[1]) - time_to_num(start_end[0])
        all_times.append((times_comps[i], start, dur))

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
