from unittest import TestCase

from players_data_helpers import insert_players_into_database
from scoreboard_helpers import *


class TestSchedule(TestCase):
    def setUp(self):
        pass

    def test_given_message_call_insert_players_into_database_players_in_DB(self):
        raw = ["Abhimanyu", "Patel,", "A,", "Berndt", "DasBrot,", "B,", "Chiman Lal,", "C"]
        players = insert_players_into_database(raw)
        initial_scoreboard = ['A', '1', 'B', '0', 'C', '-1']
        scoreboard = initialize_scoreboard(initial_scoreboard, players)
        print_scoreboard(scoreboard, players)
