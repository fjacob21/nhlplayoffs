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
    predictions = restore_db(year)
    #check if round 1 is started
    if matchups.is_round_started(year, 1) or not players.is_valid_player(player):
        return False
    prediction = {'player':player, 'winner':winner}
    predictions['winners'].append(prediction)
    #Store in DB
    return store_db(year, predictions)

def get_winners(year, round=0):
    predictions = restore_db(year)
    matchups = predictions['matchups']
    if round == 0:
        return matchups
    result = []
    for matchup in matchups:
        if matchup['round'] == round:
            result.append(matchup)
    return result

#add prediction
def add(player, year, round, home, away, winner, games):
    predictions = restore_db(year)

    if not players.is_valid_player(player):
        return False

    matchup = matchups.get_matchup(year, home, away)
    if matchup is None:
        return False

    #if matchups.is_matchup_started(matchup):
    #    return False

    prediction = get_prediction(player, year, round, home, away)
    if prediction is not None:
        return update(player, year, round, home, away, winner, games)

    prediction = {'player':player, 'round':round, 'home':home, 'away':away, 'winner':winner, 'games':games}
    predictions['matchups'].append(prediction)

    #Store in DB
    return store_db(year, predictions)

#update prediction
def update(player, year, round, home, away, winner, games):
    predictions = restore_db(year)

    if not players.is_valid_player(player):
        return False

    matchup = matchups.get_matchup(year, home, away)
    if matchup is None:
        return False

    if matchups.is_matchup_started(matchup):
        return False

    prediction = get_prediction(player, year, round, home, away)
    if prediction is None:
        return False

    prediction['winner'] = winner
    prediction['games'] = games

    #Store in DB
    return store_db(year, predictions)

def get_all(year):
    predictions = restore_db(year)
    return predictions['matchups']

def get_prediction(player, year, round, home, away):
    matchups = get_all(year)
    for matchup in matchups:
        if (matchup['player'] == player and matchup['round'] == round and
        matchup['home'] == home and matchup['away'] == away):
            return matchup
    return None
