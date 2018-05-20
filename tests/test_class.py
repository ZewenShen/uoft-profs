import sys
sys.path.append("../src/selection-recommendation")
sys.path.append("../src/util")
import time_conflicts_check
import recommend
import cost


class TestClass():
    def test_time_to_num_1(self):
        assert time_conflicts_check.time_to_num("9:00") == 9

    def test_time_to_num_2(self):
        assert time_conflicts_check.time_to_num("21:00") == 21

    def test_time_to_num_3(self):
        assert time_conflicts_check.time_to_num("12:30") == 12.5

    def test_process_times_1(self):
        assert time_conflicts_check.process_times("MONDAY 18:00-20:00 THURSDAY 18:00-21:00") == [("MONDAY", 18, 2), ("THURSDAY", 18, 3)]

    def test_process_times_2(self):
        assert time_conflicts_check.process_times("WEDNESDAY 13:30-15:00") == [("WEDNESDAY", 13.5, 1.5)]

    def test_no_time_conflict_1(self):
        assert not time_conflicts_check.no_time_conflict("MONDAY 18:00-20:00 THURSDAY 18:00-21:00", "MONDAY 17:00-19:00")

    def test_no_time_conflict_2(self):
        assert time_conflicts_check.no_time_conflict("MONDAY 18:00-20:00 THURSDAY 18:00-21:00", "MONDAY 17:00-18:00")

    def test_no_time_conflict_3(self):
        assert time_conflicts_check.no_time_conflict("MONDAY 18:00-20:00", "TUESDAY 18:00-20:00")

    def test_no_time_conflict_4(self):
        assert not time_conflicts_check.no_time_conflict("MONDAY 9:00-12:00", "MONDAY 7:00-8:00 MONDAY 10:00-11:00")

    def test_no_time_conflict_5(self):
        assert not time_conflicts_check.no_time_conflict("MONDAY 18:00-20:00", "MONDAY 19:00-20:00")

    def test_no_time_conflict_6(self):
        assert time_conflicts_check.no_time_conflict("MONDAY 12:00-14:00 MONDAY 12:00-13:00", "TUESDAY 9:00-10:00")

    def test_day_to_int_1(self):  # idk why I need this
        assert recommend.day_to_int("MONDAY") == 0

    def test_day_to_int_2(self):  # idk why I need this
        assert recommend.day_to_int("THURSDAY") == 3

    def test_process_schedule_1(self):
        correct_output = [
               [None, None, None, None, None, None, None, None, None, None, ('CSC148', 'Lec 5101'), ('CSC148', 'Lec 5101'), None, None],
               [None, None, None, None, None, None, None, None, None, None, ('CSC165', 'Lec 5101'), ('CSC165', 'Lec 5101'), ('CSC165', 'Lec 5101'), None],
               [None, None, None, None, None, None, None, None, None, None, ('CSC165', 'Lec 5101'), ('CSC165', 'Lec 5101'), None, None],
               [None, None, None, None, None, None, None, None, None, None, ('CSC148', 'Lec 5101'), ('CSC148', 'Lec 5101'), ('CSC148', 'Lec 5101'), None],
               [None, None, None, None, None, None, None, None, None, None, None, None, None, None]
           ]
        assert recommend.process_schedule(
            "MONDAY 18:00-20:00 THURSDAY 18:00-21:00 TUESDAY 18:00-21:00 WEDNESDAY 18:00-20:00",
            "CSC148 Lec 5101 CSC148 Lec 5101 CSC165 Lec 5101 CSC165 Lec 5101") == correct_output

    def test_process_schedule_2(self):
        correct_output = []
        none = [None]*14
        for i in range(5):
            correct_output.append(none[:])
        assert recommend.process_schedule("", "") == correct_output

    def test_combined_instructor_score_1(self):
        assert cost.combined_instructor_score([[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]]) == 80

    def test_combined_instructor_score_2(self):
        assert cost.combined_instructor_score([[3.7, 4.1, 4, 4.2, 3.9, 3.9], [4, 3.8, 3.7, 3.8, 4.1, 3.7], [4, 3.5, 3.9, 4.2, 4.1, 3.9]]) == 78.33333333333333

    def test_combined_instructor_score_3(self):
        assert cost.combined_instructor_score([[0, 0, 0, 0, 0, 0]]) == 0
