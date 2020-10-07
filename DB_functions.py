import os
import pickle

import DB
from config import PERSISTENCE_PATH


def load_all_data_from_database():
    load_scoreboard()
    load_schedule()
    load_team_mappings()
    load_players()


def load_scoreboard():
    scoreboard_path = PERSISTENCE_PATH + '/' + 'scoreboard.pickle'
    if os.path.exists(scoreboard_path) and os.path.getsize(scoreboard_path) > 0:
        with open(scoreboard_path, 'rb') as f:
            DB.scoreboard = pickle.load(f)
    return DB.scoreboard


def write_scoreboard(scoreboard):
    if scoreboard is None:
        raise ValueError("scoreboard cannot be None")
    with open(PERSISTENCE_PATH + '/' + 'scoreboard.pickle', 'wb') as f:
        pickle.dump(scoreboard, f)


def load_schedule():
    schedule_path = PERSISTENCE_PATH + '/' + 'schedule.pickle'
    if os.path.exists(schedule_path) and os.path.getsize(schedule_path) > 0:
        with open(schedule_path, 'rb') as f:
            DB.schedule = pickle.load(f)
    return DB.schedule


def load_team_mappings():
    team_mappings_path = PERSISTENCE_PATH + '/' + 'team_mappings.pickle'
    if os.path.exists(team_mappings_path) and os.path.getsize(team_mappings_path) > 0:
        with open(team_mappings_path, 'rb') as f:
            DB.team_mappings = pickle.load(f)
    return DB.team_mappings


def load_players():
    players_path = PERSISTENCE_PATH + '/' + 'players.pickle'
    if os.path.exists(players_path) and os.path.getsize(players_path) > 0:
        with open(players_path, 'rb') as f:
            DB.players = pickle.load(f)
    return DB.players


def write_players(players):
    if players is None:
        raise ValueError("players cannot be None")
    with open(PERSISTENCE_PATH + '/' + 'players.pickle', 'wb') as f:
        pickle.dump(players, f)