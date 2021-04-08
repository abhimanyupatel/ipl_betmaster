import os
from dotenv import load_dotenv

from DB_functions import load_all_data_from_database
import telegram
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters

# setup logging
from scoreboard_helpers import scoreboard_table
from setup_methods import init_schedule, add_players, init_scoreboard
from update_methods import scoreboard, bet, wa_bets, get_matches, next_round, match_winners, current_bets

PORT = int(os.environ.get('PORT', 5000))


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I cannot converse but how can I help? I am here to serve.")


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def main():
    bot = telegram.Bot(token=os.environ['TOKEN'])
    updater = Updater(token=os.environ['TOKEN'], use_context=True)
    dispatcher = updater.dispatcher

    # load from pickle files
    load_all_data_from_database()

    start_handler = CommandHandler('start', echo)
    dispatcher.add_handler(start_handler)

    init_handler = CommandHandler('init', init_schedule, Filters.user(username="@abhimanyu_patel"))
    dispatcher.add_handler(init_handler)

    add_players_handler = CommandHandler('addPlayers', add_players)
    dispatcher.add_handler(add_players_handler)

    init_scoreboard_handler = CommandHandler('initScoreboard', init_scoreboard,
                                             Filters.user(username="@abhimanyu_patel"))
    dispatcher.add_handler(init_scoreboard_handler)

    bet_handler = CommandHandler('bet', bet)
    dispatcher.add_handler(bet_handler)

    multi_bet_handler = CommandHandler('multiBet', wa_bets)
    dispatcher.add_handler(multi_bet_handler)

    scoreboard_handler = CommandHandler('scoreboard', scoreboard)
    dispatcher.add_handler(scoreboard_handler)

    current_bet_handler = CommandHandler('currentBets', current_bets)
    dispatcher.add_handler(current_bet_handler)

    next_matches_handler = CommandHandler('getNextMatches', get_matches)
    dispatcher.add_handler(next_matches_handler)

    next_round_handler = CommandHandler('nextRound', next_round)
    dispatcher.add_handler(next_round_handler)

    match_winner_handler = CommandHandler('matchWinners', match_winners, Filters.user(username="@abhimanyu_patel"))
    dispatcher.add_handler(match_winner_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # must be last handler
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    # start listening to messages
    if os.getenv('LOCAL') is not None and os.environ['LOCAL']:
        updater.start_polling()
    else:
        updater.start_webhook(listen="0.0.0.0",
                              port=int(PORT),
                              url_path=os.environ['TOKEN'])
        updater.bot.setWebhook('https://bb-ipl-betmaster.herokuapp.com/' + os.environ['TOKEN'])

    print(bot.get_me())
    print('Hello')


if __name__ == '__main__':
    load_dotenv()
    main()
