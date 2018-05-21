import sys
import unittest
sys.path.append("../src/util")
import Database

class Test(unittest.TestCase):
    def setUp(self):
        self.db = Database.get_connection_with_dictcursor('../database.info', 'uoftcourses')
        self.cursor = self.db.cursor()

    def tearDown(self):
        self.db.close()

    def test_get_prof_quality(self):
        assert Database.get_prof_quality_by_fullname(self.cursor, "David Liu") == {'average_enthusiasm': 4.47, 'average_course_atmosphere': 4.41}

if __name__ == '__main__':
    unittest.main()
