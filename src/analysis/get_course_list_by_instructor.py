import sys
sys.path.append('../util/')
import Database
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('instructor', help = "The full name of instructor")
    parser.add_argument('campus', help = "The campus where the instructor stays")
    args = parser.parse_args()

    instructorFullName = args.instructor
    campus = args.campus

    connection = Database.get_connection_with_dict_cursor('../../database.info', 'uoftcourses')
    dict_cursor = connection.cursor()

    print(Database.get_course_list_by_instructor(dict_cursor, instructorFullName, campus))
    sys.stdout.flush()
