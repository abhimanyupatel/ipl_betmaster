import pickle
import DB
from DB_functions import load_players
from config import PERSISTENCE_PATH
from player import Player


def fill_from_database():
    players = dict()
    # FUTURE replace DB.players
    for alias in DB.players:
        players[alias] = DB.players[alias]
    return players


def insert_players_into_database(args):
    players = fill_from_database()
    raw = ' '.join(args)
    values = raw.split(',')
    if len(values) % 2 != 0:
        raise IOError('Invalid input')

    for x in range(0, len(values), 2):
        first_name, last_name = values[x].strip().split(' ')
        alias = values[x+1].strip()
        if alias in players:
            raise ValueError("Alias {} already exists".format(alias))

        players[alias] = Player(first_name, last_name, alias)

    return players


def get_player_by_name(name, players=None):
    if players is None:
        players = load_players()
    for player_alias in players:
        if players[player_alias].get_name() == name:
            return player_alias
    return None


def get_current_bets(players=None):
    if players is None:
        players = load_players()
    table = ""
    for k, v in players.items():
        table += "{}: {}\n".format(players[k].get_name(), ', '.join(players[k].get_current_bet()))
    return table
