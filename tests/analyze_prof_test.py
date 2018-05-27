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
        assert Database.get_prof_quality_by_instructorFullName(self.cursor, "David Liu", "St. George") == \
                        {'homework_quality': 4.2,\
                        'deeper_understanding': 4.21,\
                        'enthusiasm': 4.47,\
                        'course_atmosphere': 4.41,\
                        'homework_fairness': 4.07,\
                        'overall_quality': 4.0,\
                        'workload': 3.46}

    def test_get_avg_prof_quality_by_department(self):
        assert Database.get_avg_prof_quality_by_department(self.cursor, "CSC", "St. George") == \
                        {'homework_quality': 3.95,\
                        'deeper_understanding': 4.01,\
                        'enthusiasm': 3.95,\
                        'course_atmosphere': 3.9,\
                        'homework_fairness': 3.88,\
                        'overall_quality': 3.59,
                        'workload': 3.58}

    def test_get_past_eval_by_instructorFullName_and_cID(self):
        assert Database.get_past_eval_by_instructorFullName_and_cID(self.cursor, "David Liu", "CSC148", "St. George") == \
                        {'homework_quality': 4.28,\
                        'respondent_percentage': 0.37,\
                        'recommend_rating': 4.22,\
                        'deeper_understanding': 4.18,\
                        'intellectually_simulating': 4.08,\
                        'homework_fairness': 4.15,\
                        'overall_quality': 4.05,\
                        'workload': 3.42}

    def test_get_past_eval_by_cID_excluding_one_prof(self):
        assert Database.get_past_eval_by_cID_excluding_one_prof(self.cursor, "David Liu", "CSC148", "St. George") ==\
                        {'homework_quality': 4.13,\
                        'respondent_percentage': 0.36,\
                        'recommend_rating': 3.92,\
                        'deeper_understanding': 4.18,\
                        'intellectually_simulating': 4.08,\
                        'homework_fairness': 4.08,\
                        'overall_quality': 3.8,\
                        'workload': 3.49
                        }

if __name__ == '__main__':
    unittest.main()
