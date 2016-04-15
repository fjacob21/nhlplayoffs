# Matchups management module
#
import postgres_store
from datetime import datetime
from dateutil import tz

_db = postgres_store.get_default()

def restore_db(year):
    data = _db.restore('data', year)
    if data == '':
        data = {"matchups":{},
               "current_round":0}
    return data

def store_db(year, data):
    return _db.store('data', year, data)

#get complete data
def get(year):
    return restore_db(year)

#update complete data
def update(year, data):
    return store_db(year, data)

def get_current_round(year):
    data = get(year)
    return int(data['current_round'])

def get_matchups(year, round=0):
    data = get(year)
    if round == 0:
        return data['matchups']
    return data['matchups'][str(round)]

def get_matchup(year, home, away):
    matchups = get_matchups(year, 0)

    for round in list(matchups.values()):
        for matchup in round:
            if matchup['home']['team']['id'] == int(home) and matchup['away']['team']['id'] == int(away):
                return matchup
    return None

def parse_time(timestamp):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    utc = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    utc = utc.replace(tzinfo=from_zone)
    return utc.astimezone(to_zone)

def get_start(matchup):
    if 'start' in matchup:
        return parse_time(matchup['start'])
    return None

def now():
    to_zone = tz.gettz('America/New_York')
    return datetime.now().replace(tzinfo=to_zone)

def is_round_started(year, round):
    matchups = get_matchups(year, round)
    n = now()

    for matchup in matchups:
        start = get_start(matchup)
        if start is not None:
            if n > start:
                print('Started')
                return True
    print('not Started')
    return False

def is_matchup_started(matchup):
    n = now()
    start = get_start(matchup)
    if start is not None:
        if n > start:
            print(start,n)
            return True
    return False
