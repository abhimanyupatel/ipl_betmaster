import pickle
import psycopg2

import DB
from persistence.postgres_connection import setup_connection, close_connection


def load_all_data_from_database():
    load_scoreboard()
    load_schedule()
    load_team_mappings()
    load_players()


def load_scoreboard():
    cur, conn = setup_connection()
    cur.execute("""SELECT scoreboard FROM ipl_data""")
    data = cur.fetchone()
    close_connection(cur, conn)
    if data is not None:
        if type(data) is tuple and data[0] is not None:
            DB.scoreboard = pickle.loads(data[0])
    return DB.scoreboard


def write_scoreboard(scoreboard):
    if scoreboard is None:
        raise ValueError("scoreboard cannot be None")
    scoreboard = pickle.dumps(scoreboard)
    cur, conn = setup_connection()
    cur.execute("""UPDATE ipl_data SET scoreboard = %s WHERE year = 2021""", (psycopg2.Binary(scoreboard),))
    conn.commit()
    close_connection(cur, conn)


def load_schedule():
    cur, conn = setup_connection()
    cur.execute("""SELECT schedule FROM ipl_data""")
    data = cur.fetchone()
    close_connection(cur, conn)
    if data is not None:
        if type(data) is tuple and data[0] is not None:
            DB.scoreboard = pickle.loads(data[0])
    return DB.schedule


def load_team_mappings():
    cur, conn = setup_connection()
    cur.execute("""SELECT team_mappings FROM ipl_data""")
    data = cur.fetchone()
    close_connection(cur, conn)
    if data is not None:
        if type(data) is tuple and data[0] is not None:
            DB.scoreboard = pickle.loads(data[0])
    return DB.team_mappings


def load_players():
    cur, conn = setup_connection()
    cur.execute("""SELECT players FROM ipl_data""")
    data = cur.fetchone()
    close_connection(cur, conn)
    if data is not None:
        if type(data) is tuple and data[0] is not None:
            DB.scoreboard = pickle.loads(data[0])
    return DB.players


def write_players(players):
    if players is None:
        raise ValueError("players cannot be None")
    players = pickle.dumps(players)
    cur, conn = setup_connection()
    cur.execute("""UPDATE ipl_data SET players = %s WHERE year = 2021""", (players,))
    # cur.execute("""INSERT into ipl_data (players) VALUES (%s)""", (psycopg2.Binary(players),))
    conn.commit()
    close_connection(cur, conn)
