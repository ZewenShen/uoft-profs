import sys
sys.path.append("../util")
import numpy as np
import Database

DB_NAME = "uoftcourses"
DB_PATH = "../../database.info"


def __get_instructor_scores(instructor, cID):
    """
    instructor: a string e.g. "S Huynh", "T Fairgrieve"
    cID: a string e.g. "CSC148"
    Returns a list of length 6 with mean evaluation data with a highscore of 5, if evaluation data exists.
    Otherwise, returns None.
    """
    connection = Database.get_connection(DB_PATH, DB_NAME)
    cursor = connection.cursor()

    all_eval_data = Database.get_eval_data_by_cID_and_instructor(cursor, cID, instructor)

    if len(all_eval_data) == 0:  # no eval data for cID and instructor
        return None

    intellectually_stimulating = [i[8] for i in all_eval_data]
    deeper_understanding = [i[9] for i in all_eval_data]
    course_atmosphere = [i[10] for i in all_eval_data]
    overall_quality = [i[13] for i in all_eval_data]
    enthusiasm = [i[14] for i in all_eval_data]
    recommend = [i[16] for i in all_eval_data]
    # factors like homework fairness and workload were omitted since they are instructor-independent

    # take the mean across all terms/years
    means = []
    means.append(np.mean(intellectually_stimulating))
    means.append(np.mean(deeper_understanding))
    means.append(np.mean(course_atmosphere))
    means.append(np.mean(overall_quality))
    means.append(np.mean(enthusiasm))
    means.append(np.mean(recommend))

    return means


def all_instructor_scores(schedule):
    """
    schedule: a list of lists. This should be an output from a process_schedule() call.
    e.g. [
             [None, None, None, None, None, None, None, None, None, None, ('CSC148', 'Lec 5101'), ('CSC148', 'Lec 5101'), None, None],
             [None, None, None, None, None, None, None, None, None, None, ('CSC165', 'Lec 5101'), ('CSC165', 'Lec 5101'), ('CSC165', 'Lec 5101'), None],
             [None, None, None, None, None, None, None, None, None, None, ('CSC165', 'Lec 5101'), ('CSC165', 'Lec 5101'), None, None],
             [None, None, None, None, None, None, None, None, None, None, ('CSC148', 'Lec 5101'), ('CSC148', 'Lec 5101'), ('CSC148', 'Lec 5101'), None],
             [None, None, None, None, None, None, None, None, None, None, None, None, None, None]
         ]

    Returns a list of lists, each having length 6. Each list contains the eval data of a particular prof
    in one course.
    """
    connection = Database.get_connection(DB_PATH, DB_NAME)
    cursor = connection.cursor()

    instructor_scores = []
    seen = set()

    for i in range(len(schedule)):
        for j in range(len(schedule[0])):
            if schedule[i][j] and schedule[i][j] not in seen:
                instructor = Database.get_instructor_by_cID_and_lecNum(cursor, schedule[i][j][0], schedule[i][j][1])
                instructor_score = __get_instructor_scores(instructor, schedule[i][j][0])

                # we can safely ignore sections without instructors (e.g. practicals) since __get_instructor_scores() will simply return None
                if instructor_score:
                    instructor_scores.append(instructor_score)

                seen.add(schedule[i][j])

    return instructor_scores


def combined_instructor_score(instructor_scores):
    """
    instructor_scores: a list of lists, each having length 6. Each list contains the eval data of a particular prof
    in one course.
    Returns a number, representing the combined instructor score in percent. This number is calculated simply
    by summing all the scores and dividing by the maximum total score that can be achieved (since I'm not a statistician
    and this is the best thing I could think of). If no instructor scores are available, returns 0.

    e.g. combined_instructor_score([[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]]) -> 80.0
         combined_instructor_score([[3.7, 4.1, 4, 4.2, 3.9, 3.9], [4, 3.8, 3.7, 3.8, 4.1, 3.7], [4, 3.5, 3.9, 4.2, 4.1, 3.9]]) -> 78.33333333333333
         combined_instructor_score([]) -> None
    """
    if instructor_scores == []:  # no eval data for any courses
        return 0

    total = np.sum(instructor_scores)
    max_score = 5*6*len(instructor_scores)  # scores are out of 5, 6 factors are being considered (see __get_instructor_scores())
    return 100*total/max_score
