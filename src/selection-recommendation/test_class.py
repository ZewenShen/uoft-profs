import time_conflicts_check

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
    