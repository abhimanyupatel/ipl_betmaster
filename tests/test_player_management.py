from unittest import TestCase

from players_data_helpers import insert_players_into_database


class TestSchedule(TestCase):
    def setUp(self):
        pass

    def test_given_message_call_insert_players_into_database_players_in_DB(self):
        raw = ["Abhimanyu", "Patel,", "A,", "Berndt", "DasBrot,", "BDB"]
        players = insert_players_into_database(raw)
        self.assertEqual(len(players), 2)
        self.assertIn("A", players)
        self.assertIn("BDB", players)
