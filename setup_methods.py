import logging
import pickle

import DB
import logger_config
from DB_functions import load_players, write_scoreboard, write_players
from config import PERSISTENCE_PATH
from players_data_helpers import insert_players_into_database
from schedule_extraction_helpers import read_schedule
from scoreboard_helpers import initialize_scoreboard, scoreboard_table


def init_schedule(update, context):
    if len(context.args) > 0:
        logger_config.logger.log(logging.INFO, "Extra arguments have been discarded")
    DB.schedule, DB.team_mappings = read_schedule()

    with open(PERSISTENCE_PATH + '/' + 'schedule.pickle', 'wb') as f:
        pickle.dump(DB.schedule, f)
    with open(PERSISTENCE_PATH + '/' + 'team_mappings.pickle', 'wb') as f:
        pickle.dump(DB.team_mappings, f)

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
