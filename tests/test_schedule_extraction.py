from unittest import TestCase

from schedule_extraction_helpers import *


class TestSchedule(TestCase):
    def setUp(self):
        pass

    def test_given_valid_row_call_init_schedule_return_correct_data(self):
        row = [1, "Mumbai Indians (MI) Vs Chennai Super Kings (CSK)", "19.Sep.20"",Saturday", "7:30 PM IST",
               "6:00 PM UAE", "ABU DHABI"]
        match_no, teams, date, ist, swiss_time = get_parameters(row)
        full_team1, full_team2, short_team1, short_team2 = get_team_information(teams)
        self.assertEqual(full_team1, 'Mumbai Indians')
        self.assertEqual(short_team1, 'MI')
        self.assertEqual(full_team2, 'Chennai Super Kings')
        self.assertEqual(short_team2, 'CSK')

    def test_given_invalid_row_call_init_schedule_return_no_data(self):
        row = [57, "Qualifier-1", "TBD", "TBD", "7:30 PM IST", "6:00 PM UAE", "TBD"]
        match_no, teams, date, ist, swiss_time = get_parameters(row)
        full_team1, full_team2, short_team1, short_team2 = get_team_information(teams)
        self.assertEqual(full_team1, '')
        self.assertEqual(short_team1, '')
        self.assertEqual(full_team2, '')
        self.assertEqual(short_team2, '')

    def test_call_read_schedule_return_filled_schedule(self):
        schedule, team_mappings = read_schedule()
        self.assertEqual(len(team_mappings), 8)
        self.assertEqual(len(schedule), 60)

    def test_get_next_matches(self):
        get_next_matches()
