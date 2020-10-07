import pickle

import DB
from DB_functions import load_team_mappings, load_players, write_players
from players_data_helpers import get_player_by_name


def upsert_bet(args):
    if len(args) < 2 or len(args) > 3:
        raise ValueError("Invalid message format. Only use 'alias/name' 'team1' [team2] ")

    players = load_players()
    identifier = args[0]
    bet_team = [x[:-1].upper() if ',' == x[-1] else x.upper() for x in args[1:]]

    if identifier not in DB.players:
        identifier = get_player_by_name(identifier, players)
        if identifier is None:
            raise ValueError("This player does not exist")

    players[identifier].clear_current_bet()
    players[identifier].set_current_bet(bet_team)
    write_players(players)
    return identifier


def extract_from_wa_messages(raw, team_mappings=None):
    if team_mappings is None:
        team_mappings = load_team_mappings()
    raw = [x for x in raw if not ('[' in x or ']' in x)]
    raw = [x[:-1] if ',' == x[-1] else x for x in raw]
    i = 0
    player_bets = dict()
    cur_player = ""
    in_teams = False
    while i < len(raw):
        cur_player += ' ' + raw[i]
        if ':' == cur_player[-1]:
            cur_player = cur_player[:-1].strip()
            player_bets[cur_player] = set()
        i += 1
        while i < len(raw) and raw[i].upper() in team_mappings:
            in_teams = True
            player_bets[cur_player].add(raw[i].upper())
            i += 1

        if in_teams:
            cur_player = ""
            in_teams = False
    return player_bets
