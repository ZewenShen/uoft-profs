import sys
sys.path.append("../src/course_selection")
sys.path.append("../src/util")
import selection_utils 
import unittest


class TestClass(unittest.TestCase):
    def test_time_to_num_1(self):
        assert selection_utils.time_to_num("21:00") == 42 

    def test_time_to_num_2(self):
        assert selection_utils.time_to_num("12:30") == 25

    def test_num_to_time_1(self):
        assert selection_utils.num_to_time(40) == '20:00'

    def test_num_to_time_2(self):
        assert selection_utils.num_to_time(41) == '20:30'

    def test_process_times_1(self):
        assert selection_utils.process_times("WEDNESDAY 18:00-21:00") == {'WEDNESDAY': [(36, 42)], 'FRIDAY': [], 'TUESDAY': [], 'MONDAY': [], 'THURSDAY': []}

    def test_process_times_2(self):
        assert selection_utils.process_times("WEDNESDAY 18:00-21:00 THURSDAY 13:30-15:00") == {'WEDNESDAY': [(36, 42)], 'FRIDAY': [], 'TUESDAY': [], 'MONDAY': [], 'THURSDAY': [(27, 30)]}

    def test___process_raw_course_data(self):
        test = [['CSC148H1', 'Lec 0101', 'TUESDAY 10:00-12:00 FRIDAY 10:00-11:00'],
                ['CSC148H1', 'Lec 0102', 'TUESDAY 10:00-12:00 FRIDAY 10:00-11:00'], 
                ['CSC148H1', 'Tut 0101', 'THURSDAY 09:00-11:00'], 
                ['CSC148H1', 'Tut 0201', 'THURSDAY 11:00-13:00'], 
                ['CSC148H1', 'Tut 0301', 'THURSDAY 13:00-15:00'], 
                ['CSC148H1', 'Tut 5101', 'THURSDAY 19:00-21:00']]
        selection_utils._process_raw_course_data(test)
        assert test == [['CSC148H1', 'Lec 0101', {'TUESDAY': [(20, 24)],
            'WEDNESDAY': [], 'FRIDAY': [(20, 22)], 'MONDAY': [], 'THURSDAY':
            []}], ['CSC148H1', 'Lec 0102', {'TUESDAY': [(20, 24)], 'WEDNESDAY':
                [], 'FRIDAY': [(20, 22)], 'MONDAY': [], 'THURSDAY': []}],
            ['CSC148H1', 'Tut 0101', {'TUESDAY': [], 'WEDNESDAY': [], 'FRIDAY':
                [], 'MONDAY': [], 'THURSDAY': [(18, 22)]}], ['CSC148H1', 'Tut 0201', {'TUESDAY': [], 'WEDNESDAY': [], 'FRIDAY': [],
                        'MONDAY': [], 'THURSDAY': [(22, 26)]}], ['CSC148H1',
                            'Tut 0301', {'TUESDAY': [], 'WEDNESDAY': [],
                                'FRIDAY': [], 'MONDAY': [], 'THURSDAY': [(26,
                                    30)]}], ['CSC148H1', 'Tut 5101', {'TUESDAY':
                                        [], 'WEDNESDAY': [], 'FRIDAY': [],
                                        'MONDAY': [], 'THURSDAY': [(38, 42)]}]]
    def test__is_not_valid(self):
    	item = (['CSC148H1', 'Lec 0101', {'WEDNESDAY': [], 'TUESDAY': [(20, 24)], 'FRIDAY': [(20, 22)], 'MONDAY': [], 'THURSDAY': [(26, 30)]}], ['CSC148H1', 'Tut 0301', {'WEDNESDAY': [], 'TUESDAY': [], 'FRIDAY': [], 'MONDAY': [], 'THURSDAY': [(26, 30)]}])
    	assert selection_utils._is_not_valid(item) is True
    	


if __name__ == '__main__':
    unittest.main()
