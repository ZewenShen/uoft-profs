import sys
sys.path.append('../util/')
import Database
import pandas as pd
import matplotlib.pyplot as plt

PROF_QUALITY_BY_PNAME = 1 # index of DB_GETMETHOD_WITH_ONE_ARG
DEPARTMENT_QUALITY_BY_DID = 2 # index of DB_GETMETHOD_WITH_ONE_ARG
COURSE_EVAL_BY_INSTRUCTOR_AND_CID = 3 # index of DB_GETMETHOD_WITH_TWO_ARGS
COURSE_EVAL_BY_CID_EXCLUDING_PROF = 4 # index of DB_GETMETHOD_WITH_TWO_ARGS
COURSE_EVAL_BY_CID = 5

DB_GETMETHOD_WITH_ONE_ARG = {\
    PROF_QUALITY_BY_PNAME: Database.get_prof_quality_by_instructorFullName,\
    DEPARTMENT_QUALITY_BY_DID: Database.get_avg_prof_quality_by_department,\
    COURSE_EVAL_BY_CID: Database.get_past_eval_by_cID
} # used by __analyze_data_by_DB_GETMETHOD_DICT
   
"""
DB_GETMETHOD_WITH_TWO_ARGS = {\
    COURSE_EVAL_BY_PROF_AND_CID: Database.get_past_eval_by_instructorFullName_and_cID,\
    COURSE_EVAL_BY_CID_EXCLUDING_PROF: Database.get_past_eval_by_cID_excluding_one_prof
}
"""



def __analyze_data_by_DB_GETMETHOD_WITH_ONE_ARG(get_type, dict_cursor, arg):
    """
    A generalized helper function used to return DataFrame
    """
    data = DB_GETMETHOD_WITH_ONE_ARG[get_type](dict_cursor, arg)
    df = pd.DataFrame(list(data.values()), columns=[arg], index=list(data.keys()))
    return df

"""
def __analyze_data_by_DB_GETMETHOD_WITH_TWO_ARGS(get_type, dict_cursor, *args):
    assert len(args) == 2
    data = DB_GETMETHOD_WITH_TWO_ARGS[get_type](dict_cursor, args[1], args[2])
    df = pd.DataFrame(list(data.values()), columns=[args[0]], index=list(data.keys()))
    return df
"""

def analyze_prof_quality_by_instructorFullName(dict_cursor, instructorFullName):
    """
    >>> analyze_prof_quality_by_instructorFullName(dict_cursor, 'David Liu')
                               David Liu
    average_enthusiasm              4.47
    average_course_atmosphere       4.41
    """
    return __analyze_data_by_DB_GETMETHOD_WITH_ONE_ARG(PROF_QUALITY_BY_PNAME, dict_cursor, instructorFullName)

def analyze_avg_prof_quality_by_department(dict_cursor, departmentID):
    """
    >>> analyze_avg_prof_quality_by_department(dict_cursor, 'CSC')
                                CSC
    average_enthusiasm         3.95
    average_course_atmosphere  3.90

    """
    return __analyze_data_by_DB_GETMETHOD_WITH_ONE_ARG(DEPARTMENT_QUALITY_BY_DID, dict_cursor, departmentID)

def analyze_past_eval_by_instructorFullName_and_cID(dict_cursor, instructorFullName, cID):
    """
    >>> analyze_past_eval_by_instructorFullName_and_cID(dict_cursor, 'David Liu', 'CSC148')
                                       David Liu's CSC148
        avg_overall_quality                          4.05
        avg_intellectually_simulating                4.08
        avg_homework_fairness                        4.15
        avg_respondent_percentage                    0.37
        avg_deeper_understanding                     4.18
        avg_recommend_rating                         4.22
        avg_home_quality                             4.28

    """
    course_by_prof_eval_data = Database.get_past_eval_by_instructorFullName_and_cID(dict_cursor,\
            instructorFullName, cID)
    
    course_by_prof_df = pd.DataFrame(list(course_by_prof_eval_data.values()), columns =\
            ["{}'s {}".format(instructorFullName, cID)], index=list(course_by_prof_eval_data.keys()))

    return course_by_prof_df

def analyze_past_eval_by_cID(dict_cursor, cID):
    """
    >>> analyze_past_eval_by_cID(dict_cursor, 'CSC265')
                                       CSC265
        avg_overall_quality              4.47
        avg_intellectually_simulating    4.68
        avg_homework_fairness            4.42
        avg_respondent_percentage        0.55
        avg_deeper_understanding         4.63
        avg_recommend_rating             4.23
        avg_home_quality                 4.63

    """
    return __analyze_data_by_DB_GETMETHOD_WITH_ONE_ARG(COURSE_EVAL_BY_CID, dict_cursor, cID)

def analyze_past_eval_by_cID_excluding_one_prof(dict_cursor, exclusiveInstructorFullName, cID):
    """
    >>> analyze_past_eval_by_cID_excluding_one_prof(dict_cursor, 'Faith Ellen', 'CSC240')
                          CSC240 not taught by Faith Ellen
    avg_recommend_rating                              3.40
    avg_deeper_understanding                          4.10
    avg_intellectually_simulating                     4.00
    avg_homework_fairness                             3.90
    avg_home_quality                                  4.00
    avg_overall_quality                               3.30
    avg_respondent_percentage                         0.39
    """
    course_by_prof_eval_data = Database.get_past_eval_by_cID_excluding_one_prof(dict_cursor,\
            exclusiveInstructorFullName, cID)
    
    course_by_prof_df = pd.DataFrame(list(course_by_prof_eval_data.values()), columns =\
            ["{} not taught by {}".format(cID, exclusiveInstructorFullName)], index=list(course_by_prof_eval_data.keys()))

    return course_by_prof_df

def get_dataframe_by_contrasting_prof_with_department(dict_cursor, instructorFullName, departmentID):
    """
    The major method (1 of 2) we used in this file.
    """
    df1 = analyze_prof_quality_by_instructorFullName(dict_cursor, instructorFullName)
    df2 = analyze_avg_prof_quality_by_department(dict_cursor, departmentID)
    df = __concat_two_dataframes(df1, df2)
    __get_bar_by_dataframe(df, title="Prof {} vs {} department".format(instructorFullName, departmentID))

def get_dataframe_by_contrasting_prof_with_other_profs(dict_cursor, instructorFullName, cID):
    """
    The major method (2 of 2) we used in this file.
    """
    df1 = analyze_past_eval_by_instructorFullName_and_cID(dict_cursor, instructorFullName, cID)
    df2 = analyze_past_eval_by_cID_excluding_one_prof(dict_cursor, instructorFullName, cID)
    df = __concat_two_dataframes(df1, df2)
    __get_bar_by_dataframe(df, title="Prof {} vs other profs who taught {}".format(instructorFullName, cID))

def __concat_two_dataframes(df1, df2):
    """
    A helper function used to combine two DataFrame, such that we can plot them
    together.
    """
    return pd.concat([df1, df2], axis=1)

def __get_bar_by_dataframe(df, title=None):
    df.plot(kind='bar', rot=0, alpha=0.75, title=title)
    plt.show()

if __name__ == '__main__':
    connection = Database.get_connection_with_dict_cursor('../../database.info', 'uoftcourses')
    dict_cursor = connection.cursor()
