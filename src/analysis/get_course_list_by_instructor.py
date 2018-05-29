import sys
sys.path.append('../util/')
import Database
import argparse
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('instructor', help = "The full name of instructor")
    parser.add_argument('campus', help = "The campus where the instructor stays")
    args = parser.parse_args()

    instructorFullName = args.instructor
    campus = args.campus

    connection = Database.get_connection_with_dict_cursor('../../database.info', 'uoftcourses')
    dict_cursor = connection.cursor()

    course_list = Database.get_course_list_by_instructor(dict_cursor, instructorFullName, campus)
    json_course_list = json.dumps(course_list)
    print(json_course_list)
    sys.stdout.flush()
