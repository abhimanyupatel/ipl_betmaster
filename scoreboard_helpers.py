import DB
from DB_functions import load_players, load_scoreboard, load_team_mappings, write_players, write_scoreboard


def initialize_scoreboard(scoreboard_data=None, players=None):
    if players is None:
        players = load_players()
    scoreboard = dict()
    empty_scoreboard = scoreboard_data is None or len(scoreboard_data) == 0
    if empty_scoreboard:
        for alias in players:
            scoreboard[alias] = 0
    else:
        if len(scoreboard_data) % 2 != 0:
            raise IOError('Invalid number of arguments')
        else:
            for i in range(0, len(scoreboard_data), 2):
                alias = scoreboard_data[i].strip()
                score = int(scoreboard_data[i + 1])
                if alias not in players:
                    raise ValueError("{} not a valid alias for player".format(alias))
                scoreboard[alias] = score

    return scoreboard


def scoreboard_table(scoreboard=None, players=None):
    if scoreboard is None:
        scoreboard = load_scoreboard()
    if players is None:
        players = load_players()

    table = ""
    for k, v in sorted(scoreboard.items(), key=lambda item: item[1], reverse=True):
        table += "{}: {}\n".format(players[k].get_name(), int(v))
    return table


def print_scoreboard(scoreboard=None, players=None):
    print(scoreboard_table(scoreboard, players))


def update_scoreboard(winning_teams):
    teams = load_team_mappings()
    players = load_players()
    scoreboard = load_scoreboard()
    if len(winning_teams) == 0 or len(winning_teams) > 2:
        raise ValueError("Please define the winning teams")
    winners = set(''.join(winning_teams).split(','))
    if not winners.intersection(teams.keys()) == winners:
        raise ValueError("Non-existing teams won, please retry")

    for alias in players:
        bets = players[alias].get_current_bet()
        if len(bets) == 0:
            correct = -1
        else:
            correct = len(bets.intersection(winners))
        scoreboard[alias] += correct
        players[alias].clear_current_bet()

    # write players to disk
    write_players(players)

    # write scoreboard to disk
    write_scoreboard(scoreboard)
