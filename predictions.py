# Predictions management module
#
from postgres_store import postgres_store
import matchups
import players

_db = postgres_store('fred', 'fred', '763160', 'localhost', 5432)

def restore_db(year):
    predictions = _db.restore('predictions', year)
    if predictions == '':
        predictions = {'matchups':[],
                       'winners':[]}
    return predictions

def store_db(year, predictions):
    return _db.store('predictions', year, predictions)

#add big winner prediction
def add_winner(player, year, winner):
    playpredictionsers = restore_db()
    #check if round 1 is started
    if matchups.is_round_started(year, 1) or not players.is_valid_player(player):
        return False
    prediction = {'player':player, 'winner':winner}
    playpredictionsers['winners'].append(prediction)
    #Store in DB
    return store_db(plpredictionsayers)

#add prediction
def add(player, year, round, home, away, winner, games):
    playpredictionsers = restore_db()

    if matchups.is_round_started(year, round) or not players.is_valid_player(player):
        return False
    prediction = {'player':player, 'round':round, 'home':home, 'away':away, 'winner':winner, 'games':games}
    playpredictionsers['matchups'].append(prediction)
    #Store in DB
    return store_db(plpredictionsayers)

#update prediction
def update(player, year, round, home, away, winner, games):
    playpredictionsers = restore_db()

    #players[hname] = {'name':name, 'psw':hpsw, 'email':email, 'admin':admin}
    #Store in DB
    return store_db(plpredictionsayers)

def get_all():
    playpredictionsers = restore_db()
    return ''

def get(player):
    playpredictionsers = restore_db()
    hname = userhash(player)
    return ''
