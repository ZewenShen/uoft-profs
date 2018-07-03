import argparse
import selection_impl
import sys
sys.path.append('../util')
import Database

PATH = '../../database.info'
DB_NAME = 'uoftcourses'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id', nargs = '+', help = "The id of course, e.g., CSC240")
    parser.add_argument('-t', '--term', required = True, help = "The term you want to schedule for")
    args = parser.parse_args()

    db = Database.get_connection(PATH, DB_NAME)
    with db.cursor() as cursor:
        unfiltered_result = selection_impl.get_courses_arrangement_for_multiple_courses(cursor, args.id, args.term)
        filtered_result = selection_impl.filter_arrangement_result(unfiltered_result)
        print(filtered_result)


