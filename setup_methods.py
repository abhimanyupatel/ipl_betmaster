import logging
import pickle
import os

import psycopg2

import DB
import logger_config
from DB_functions import load_players, write_scoreboard, write_players
from persistence.postgres_connection import setup_connection, close_connection
from players_data_helpers import insert_players_into_database
from schedule_extraction_helpers import read_schedule
from scoreboard_helpers import initialize_scoreboard, scoreboard_table


def init_schedule(update, context):
    if len(context.args) > 0:
        logger_config.logger.log(logging.INFO, "Extra arguments have been discarded")
    DB.schedule, DB.team_mappings = read_schedule()

    schedule = pickle.dumps(DB.schedule)
    team_mappings = pickle.dumps(DB.team_mappings)
    cur, conn = setup_connection()
    cur.execute("""UPDATE ipl_data SET schedule = %s WHERE year = 2021""", (psycopg2.Binary(schedule), ))
    cur.execute("""UPDATE ipl_data SET team_mappings = %s WHERE year = 2021""", (psycopg2.Binary(team_mappings),))
    conn.commit()
    close_connection(cur, conn)

    context.bot.send_message(chat_id=update.effective_chat.id, text='Initialized Schedule')


def init_scoreboard(update, context):
    try:
        DB.scoreboard = initialize_scoreboard(context.args)
        write_scoreboard(DB.scoreboard)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Initialized scoreboard')
        context.bot.send_message(chat_id=update.effective_chat.id, text=scoreboard_table(DB.scoreboard, load_players()))
    except IOError as error:
        context.bot.send_message(chat_id=update.effective_chat.id, text=repr(error))
    except ValueError as error:
        context.bot.send_message(chat_id=update.effective_chat.id, text=repr(error))
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text="An exception occured: {}".format(repr(e)))


def add_players(update, context):
    try:
        DB.players = insert_players_into_database(context.args)
        write_players(DB.players)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Added players')
        context.bot.send_message(chat_id=update.effective_chat.id, text="Current players: {}".format(
            ', '.join([player.get_name() for player in DB.players.values()])))
    except IOError:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Input Error: please ensure that all players '
                                                                        'are entered in the following format'
                                                                        '"first_name last_name, alias[, ..]" without '
                                                                        'quotes')
    except ValueError as error:
        context.bot.send_message(chat_id=update.effective_chat.id, text=repr(error))
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text="An exception occured: {}".format(repr(e)))
