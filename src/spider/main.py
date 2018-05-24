import sys
sys.path.append('../util')
import Database as db
import coursespider.cspider as cs
import evalspider.espider as es
import argparse

DB_NAME = 'uoftcourses'
DB_PATH = '../../database.info'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--init', help = "initialize the database", action="store_true")
    parser.add_argument('-c', '--course', help = "scrape courses offered at uoft", action = "store_true")
    parser.add_argument('-e', '--eval', help = "scrape eval data from uoft blackboard", action = "store_true")
    args = parser.parse_args()

    if args.init:
        db.init_db(DB_PATH, DB_NAME)

    if args.course:
        cs.main()

    if args.eval:
        es.main()
