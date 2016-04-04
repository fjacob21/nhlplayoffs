# Matchups management module
#
from postgres_store import postgres_store

_db = postgres_store('fred', 'fred', '763160', 'localhost', 5432)

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
    now = now()

    for matchup in matchups:
        start = get_start()
        if start is not None:
            if now > start:
                return True
    return False
