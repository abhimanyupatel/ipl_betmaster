import DB
from DB_functions import load_players
from bet_helpers import upsert_bet, extract_from_wa_messages
from players_data_helpers import get_current_bets
from schedule_extraction_helpers import get_next_matches
from scoreboard_helpers import scoreboard_table, update_scoreboard


def scoreboard(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=scoreboard_table())


def get_matches(update, context):
    if len(context.args) == 0:
        days = 1
    else:
        try:
            days = int(context.args[0])
        except Exception:
            days = 1
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_next_matches(days=days))


def bet(update, context):
    try:
        alias = upsert_bet(context.args)
        players = load_players()
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Upserted bet for {}: {}".format(players[alias].get_name(),
                                                                       ', '.join(players[alias].get_current_bet())))
    except ValueError as err:
        context.bot.send_message(chat_id=update.effective_chat.id, text=repr(err))


def wa_bets(update, context):
    player_bets = extract_from_wa_messages(context.args)
    for player in player_bets:
        upsert_bet([player] + list(player_bets[player]))
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_current_bets())


def next_round(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=scoreboard_table() + '\n' + get_next_matches())


def match_winners(update, context):
    try:
        update_scoreboard(context.args)
        next_round(update, context)
    except Exception as err:
        context.bot.send_message(chat_id=update.effective_chat.id, text=repr(err))


def current_bets(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_current_bets())
