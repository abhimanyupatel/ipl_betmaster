import csv
import logging
from datetime import datetime, timedelta
import pytz
import logger_config
from DB_functions import load_schedule, load_team_mappings
from config import PERSISTENCE_PATH, TIMEZONE


def convert_ist_to_zurich(ist_time):
    try:
        local = pytz.timezone('Europe/Zurich')
        india_tz = pytz.timezone('Asia/Calcutta')
        indian_time = datetime.strptime(ist_time, '%d.%b.%y %I:%M %p')
        indian_time = india_tz.localize(indian_time)
        return local.normalize(indian_time)
    except ValueError:
        return ist_time


def get_team_information(teams):
    teams = teams.split('Vs')
    if len(teams) <= 1:
        return '', '', '', ''

    team1 = teams[0].split('(')
    full_team1 = team1[0].strip()
    short_team1 = team1[1].strip()[:-1]
    team2 = teams[1].split('(')
    full_team2 = team2[0].strip()
    short_team2 = team2[1].strip()[:-1]
    return full_team1, full_team2, short_team1, short_team2


def get_parameters(row):
    match_no = row[0]
    teams = row[1]
    date = row[2]
    ist = date + ' ' + row[4]
    ist = ist[:-4]
    swiss_time = convert_ist_to_zurich(ist)
    return match_no, teams, date, ist, swiss_time


def read_schedule():
    team_mappings = dict()
    schedule = dict()
    with open(PERSISTENCE_PATH + '/ipl_schedule_raw.csv', newline='', encoding='utf-8-sig') as csvfile:
        raw_schedule = csv.reader(csvfile, delimiter=',')
        headers = next(raw_schedule)
        headers.append('SwissTime')
        print(headers)
        for row in raw_schedule:
            match_no, teams, date, ist, swiss_time = get_parameters(row)
            full_team1, full_team2, short_team1, short_team2 = get_team_information(teams)

            logger_config.logger.log(logging.INFO,
                                     "{}, {}, {}, {}".format(full_team1, short_team1, full_team2, short_team2))

            if short_team1 != '' and short_team1 not in team_mappings:
                team_mappings[short_team1] = full_team1
            if short_team2 != '' and short_team2 not in team_mappings:
                team_mappings[short_team2] = full_team2

            schedule[match_no] = {'home': full_team1, 'away': full_team2, 'ist': ist,
                                  'swiss_time': swiss_time, 'date': date}

    return schedule, team_mappings


def has_match_started(match_time):
    now = datetime.now(tz=pytz.timezone(TIMEZONE))
    return now > match_time


def get_next_matches(days=1, schedule=None):
    if schedule is None:
        schedule = load_schedule()
    team_mappings = {value: key for key, value in load_team_mappings().items()}
    now = datetime.now(tz=pytz.timezone(TIMEZONE))
    match_id = find_next_match(schedule, now)
    target_id = match_id
    while now + timedelta(days=days) >= schedule[str(target_id + 1)]['swiss_time']:
        target_id += 1

    matches = ""
    while match_id <= target_id:
        matches += "{}: {} ({}) vs {} ({})\n".format(schedule[str(match_id)]['swiss_time'].date(),
                                                   schedule[str(match_id)]['home'],
                                                   team_mappings[schedule[str(match_id)]['home']],
                                                   schedule[str(match_id)]['away'],
                                                   team_mappings[schedule[str(match_id)]['away']])
        match_id += 1

    return matches


def find_next_match(schedule, now=datetime.now(tz=pytz.timezone(TIMEZONE))):
    start = 1
    end = len(schedule)
    match_id = -1
    while start <= end:
        mid = (start + end) // 2
        if schedule[str(mid)]['swiss_time'] <= now:
            start = mid + 1
        else:
            match_id = mid
            end = mid - 1

    return match_id
