# Matchups management module v2
#
import postgres_store
from datetime import datetime
from dateutil import tz

_db = postgres_store.get_default()

def restore_db(year):
    data = _db.restore('datav2', year)
    if data == '':
        data = {"matchups":{},
                "teams":{},
               "current_round":0}
    else:
        teams = {}
        for m in data['teams'].items():
            teams[int(m[0])]=m[1]
        current_round = data['current_round']
        matchups = data['matchups'] #build_matchup_tree(data['matchups'])
        data = {}
        data['teams'] = teams
        data['current_round'] = current_round
        data['matchups'] = matchups
    return data

def store_db(year, data):
    return _db.store('datav2', year, data)

def get_years():
    return _db.get_rows_id('datav2')

def build_matchup_tree(raw_matchups):
    matchups = {}
    for matchup_raw in list(raw_matchups.values()):
        matchup = matchup_raw.copy()
        matchups[matchup['id']] = matchup

    for matchup in list(matchups.values()):
        next = matchup['next']
        right = matchup['right']
        left = matchup['left']
        if next in raw_matchups:
            matchup['next'] = matchups[next]
        if right in raw_matchups:
            matchup['right'] = matchups[right]
        if left in raw_matchups:
            matchup['left'] = matchups[left]
    return matchups

#get complete data
def get(year):
    return restore_db(year)

def get_teams(year=0):
    if year != 0:
        data = get(year)
        return data['teams']
    years = get_years()
    teams = {}
    for year in years:
        data = get(year)['teams']
        for team in data:
            team = int(team)
            if team not in teams:
                teams[team] = data[team]
    return teams

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
    matchups = [m for m in list(data['matchups'].values()) if m['round'] == int(round)]
    return matchups

def get_matchup(year, home, away):
    matchups = get_matchups(year, 0)

    for matchup in list(matchups.values()):
        if matchup['home'] == int(home) and matchup['away'] == int(away):
            return matchup
    return None

def parse_time(timestamp):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    utc = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    utc = utc.replace(tzinfo=from_zone)
    return utc.astimezone(to_zone)

def get_start(matchup):
    if 'start' in matchup and matchup['start']:
        return parse_time(matchup['start'])
    return None

def now():
    to_zone = tz.gettz('America/New_York')
    return datetime.now(tz.tzlocal()).astimezone(to_zone)

def is_round_started(year, round):
    matchups = get_matchups(year, round)
    n = now()

    for matchup in list(matchups):
        start = get_start(matchup)
        if start is not None:
            if n > start:
                return True
    return False

def is_matchup_started(matchup):
    n = now()
    start = get_start(matchup)
    if start is not None:
        if n > start:
            return True
    return False
