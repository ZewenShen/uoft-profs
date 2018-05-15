import sys
sys.path.append('./util')
import util.Database as db
import coursespider.cspider as cs
import evalspider.espider as es

DB_NAME = 'uoftcourses'
DB_PATH = '../../database.info'

if __name__ == '__main__':
    db.init_db(DB_PATH, DB_NAME)

    cs.main()
    es.main()
