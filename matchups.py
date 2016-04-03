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
