from unittest import TestCase

import DB
from bet_helpers import extract_from_wa_messages


class TestSchedule(TestCase):
    def setUp(self):
        pass

    def test_extract_from_wa_messages(self):
        raw = ['[19/09,', '20:27]', 'Himesh', 'Parikh:', 'Dc', '[19/09,', '20:55]', 'Sivaranjini', 'Chithambaram:',
               'KXIP', '[20/09,', '00:51]', 'Abhimanyu', 'Patel:', 'kxip,', 'dC']
        team_mappings = {'DC': 'Delhi', 'KXIP': 'Punjab'}
        player_bets = extract_from_wa_messages(raw, team_mappings)
        self.assertTrue('Himesh Parikh' in player_bets)
        self.assertTrue('Sivaranjini Chithambaram' in player_bets)
        self.assertTrue('Abhimanyu Patel' in player_bets)
        self.assertTrue(len(player_bets['Abhimanyu Patel']) == 2)
        self.assertTrue(len(player_bets['Sivaranjini Chithambaram']) == 1 and
                        "KXIP" in player_bets['Sivaranjini Chithambaram'])
