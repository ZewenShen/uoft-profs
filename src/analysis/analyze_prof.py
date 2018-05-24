import sys
sys.path.append('../util/')
import Database
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import argparse

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
   

def __analyze_data_by_DB_GETMETHOD_WITH_ONE_ARG(get_type, dict_cursor, arg):
    """
    A generalized helper function used to return DataFrame
    """
    data = DB_GETMETHOD_WITH_ONE_ARG[get_type](dict_cursor, arg)
    df = pd.DataFrame(list(data.values()), columns=[arg], index=list(data.keys()))
    return df

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
        overall_quality                          4.05
        intellectually_simulating                4.08
        homework_fairness                        4.15
        respondent_percentage                    0.37
        deeper_understanding                     4.18
        recommend_rating                         4.22
        home_quality                             4.28

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
        overall_quality              4.47
        intellectually_simulating    4.68
        homework_fairness            4.42
        respondent_percentage        0.55
        deeper_understanding         4.63
        recommend_rating             4.23
        home_quality                 4.63

    """
    return __analyze_data_by_DB_GETMETHOD_WITH_ONE_ARG(COURSE_EVAL_BY_CID, dict_cursor, cID)

def analyze_past_eval_by_cID_excluding_one_prof(dict_cursor, exclusiveInstructorFullName, cID):
    """
    >>> analyze_past_eval_by_cID_excluding_one_prof(dict_cursor, 'Faith Ellen', 'CSC240')
                      CSC240 not taught by Faith Ellen
    recommend_rating                              3.40
    deeper_understanding                          4.10
    intellectually_simulating                     4.00
    homework_fairness                             3.90
    home_quality                                  4.00
    overall_quality                               3.30
    respondent_percentage                         0.39
    """
    course_by_prof_eval_data = Database.get_past_eval_by_cID_excluding_one_prof(dict_cursor,\
            exclusiveInstructorFullName, cID)
    
    course_by_prof_df = pd.DataFrame(list(course_by_prof_eval_data.values()), columns =\
            ["{} not taught by {}".format(cID, exclusiveInstructorFullName)], index=list(course_by_prof_eval_data.keys()))

    return course_by_prof_df

def __get_dataframe_by_contrasting_prof_with_department(dict_cursor, instructorFullName, departmentID):
    """
    Get the dataframe of selected prof's evaluation and the evaluation of avg
    profs in selected department.
    """
    df1 = analyze_prof_quality_by_instructorFullName(dict_cursor, instructorFullName)
    df2 = analyze_avg_prof_quality_by_department(dict_cursor, departmentID)
    df = pd.concat([df1, df2], axis=1)
    return df

def __get_dataframe_by_contrasting_prof_with_other_profs(dict_cursor, instructorFullName, cID):
    """
    Get the dataframe of selected prof's evaluation and
    the avg evaluation of other profs who taught that course before.
    """
    df1 = analyze_past_eval_by_instructorFullName_and_cID(dict_cursor, instructorFullName, cID)
    df2 = analyze_past_eval_by_cID_excluding_one_prof(dict_cursor, instructorFullName, cID)
    df = pd.concat([df1, df2], axis=1)
    return df

def get_figure_of_dataframe_contrasting_prof_with_department(dict_cursor, ax, instructorFullName, departmentID):
    """
    Plot the prof vs avg prof in department DataFrame in python.
    """
    df = __get_dataframe_by_contrasting_prof_with_department(dict_cursor, instructorFullName, departmentID)
    #return __get_figure_by_dataframe(df, title="Prof {} vs {} department".format(instructorFullName, departmentID))
    __get_figure_by_dataframe(df, ax, title="Prof {} vs {} department".format(instructorFullName, departmentID))

def get_figure_of_dataframe_contrasting_prof_with_other_profs(dict_cursor, ax, instructorFullName, cID):
    """
    Plot the prof vs other profs DataFrame in python.
    """
    df = __get_dataframe_by_contrasting_prof_with_other_profs(dict_cursor, instructorFullName, cID)
    #return __get_figure_by_dataframe(df, title="Prof {} vs other profs who taught {}".format(instructorFullName, cID))
    __get_figure_by_dataframe(df, ax, title="Prof {} vs other profs who taught {}".format(instructorFullName, cID))

def get_figure(dict_cursor, instructorFullName, cID, departmentID):
    get_figure_of_dataframe_contrasting_prof_with_department(dict_cursor, instructorFullName, departmentID)
    get_figure_of_dataframe_contrasting_prof_with_other_profs(dict_cursor, instructorFullName, cID)
    plt.legend(loc='best')
    plt.show()

def __get_figure_by_dataframe(df, ax, title=None):
    """
    Beatify the layout of the DataFrame, add label to each bar. Then return the
    figure.
    """
    try:
        new_ax = df.plot(ax=ax, kind='bar', rot=0, alpha=0.6, title=title, figsize=(18, 11.12), fontsize=11)
        new_ax.legend(loc='best', fancybox=True, framealpha=0.5)
        for p in new_ax.patches:
            new_ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    except TypeError as e:
        print("Unable to plot. Please check your data", file=sys.stdout)
    #return plt.gcf()

def convert_figure_to_html(fig):
    """
    Convert the figure into a html tag
    """
    sio = BytesIO()
    fig.savefig(sio, format='png')
    data = base64.encodebytes(sio.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(data.replace('\n', ''))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--plot', help = "Plot the graph in GUI mod (if this flag is not set on, an html img tag will be printed to stdout)", action = "store_true")
    parser.add_argument('instructor', help = "The full name of instructor")
    parser.add_argument('courseID', help = "The id of course, e.g., CSC240")
    args = parser.parse_args()

    instructorFullName = args.instructor
    cID = args.courseID
    department = cID[0: 3]

    connection = Database.get_connection_with_dict_cursor('../../database.info', 'uoftcourses')
    dict_cursor = connection.cursor()

    fig, axes = plt.subplots(nrows=2, ncols=1)

    get_figure_of_dataframe_contrasting_prof_with_department(dict_cursor, axes[0], instructorFullName, department)
    get_figure_of_dataframe_contrasting_prof_with_other_profs(dict_cursor, axes[1], instructorFullName, cID)

    if args.plot:
        plt.show()
    else:
        fig = plt.gcf()
        print(convert_figure_to_html(fig))


