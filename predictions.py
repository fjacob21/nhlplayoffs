# Predictions management module
#
import postgres_store
import matchups
import players

_db = postgres_store.get_default()

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
    if matchups.is_round_started(year, 1):
        return False

    if not players.is_valid_player(player):
        return False

    prediction_index = get_winner_index(player, year)
    if prediction_index == -1:
        prediction = {'player':player, 'winner':winner}
        predictions['winners'].append(prediction)
    else:
        predictions['winners'][prediction_index]['winner'] = winner

    #Store in DB
    return store_db(year, predictions)

def get_winners(year):
    predictions = restore_db(year)
    winners = predictions['winners']
    return winners

def get_winner(player, year):
    winners = get_winners(year)
    for winner in winners:
        if winner['player'] == player:
            return winner
    return None

def get_winner_index(player, year):
    winners = get_winners(year)
    i = 0
    for winner in winners:
        if winner['player'] == player:
            return i
        i = i + 1
    return -1

#add prediction
def add(player, year, round, home, away, winner, games):
    predictions = restore_db(year)

    if not players.is_valid_player(player):
        return False

    matchup = matchups.get_matchup(year, home, away)
    if matchup is None:
        return False

    ####################################################
    if matchups.is_matchup_started(matchup):
        return False

    prediction_index = get_prediction_index(player, year, round, home, away)
    if prediction_index != -1:
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

    prediction_index = get_prediction_index(player, year, round, home, away)
    if prediction_index == -1:
        return False

    predictions['matchups'][prediction_index]['winner'] = winner
    predictions['matchups'][prediction_index]['games'] = games

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

def get_prediction_index(player, year, round, home, away):
    matchups = get_all(year)
    i = 0
    for matchup in matchups:
        if (matchup['player'] == player and matchup['round'] == round and
        matchup['home'] == home and matchup['away'] == away):
            return i
        i = i + 1
    return -1
