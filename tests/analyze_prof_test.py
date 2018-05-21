import sys
import unittest
sys.path.append("../src/util")
import Database

class Test(unittest.TestCase):
    """
    The Database we are using only contain evaluation data until 2017fall, so
    all the tests will fail after the database is updated sometime.
    """
    def setUp(self):
        self.db = Database.get_connection_with_dict_cursor('../database.info', 'uoftcourses')
        self.cursor = self.db.cursor()

    def tearDown(self):
        self.db.close()

    def test_get_prof_quality_by_instructorFullName(self):
        assert Database.get_prof_quality_by_instructorFullName(self.cursor, "David Liu") == {'average_enthusiasm': 4.47, 'average_course_atmosphere': 4.41}

    def test_get_avg_prof_quality_by_department(self):
        assert Database.get_avg_prof_quality_by_department(self.cursor, "CSC") == {'average_course_atmosphere': 3.9, 'average_enthusiasm': 3.95}

    def test_get_past_eval_by_instructorFullName_and_cID(self):
        assert Database.get_past_eval_by_instructorFullName_and_cID(self.cursor, "David Liu", "CSC148") == \
                        {'avg_home_quality': 4.28,\
                        'avg_respondent_percentage': 0.37,\
                        'avg_recommend_rating': 4.22,\
                        'avg_deeper_understanding': 4.18,\
                        'avg_intellectually_simulating': 4.08,\
                        'avg_homework_fairness': 4.15,\
                        'avg_overall_quality': 4.05\
                        }

    def test_get_past_eval_by_cID_excluding_one_prof(self):
        assert Database.get_past_eval_by_cID_excluding_one_prof(self.cursor, "David Liu", "CSC148") ==\
                        {'avg_home_quality': 4.13,\
                        'avg_respondent_percentage': 0.36,\
                        'avg_recommend_rating': 3.92,\
                        'avg_deeper_understanding': 4.18,\
                        'avg_intellectually_simulating': 4.08,\
                        'avg_homework_fairness': 4.08,\
                        'avg_overall_quality': 3.8\
                        }

if __name__ == '__main__':
    unittest.main()
