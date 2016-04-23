# Results management module
#
import matchups as matchups_store
import players
import predictions

def get_player_prediction(player_id, preds):
    result=[]
    for prediction in preds:
        if prediction['player'] == player_id and int(prediction['winner']) > 0:
            p = prediction.copy()
            del p['player']
            result.append(p)
    return result

def get_matchup(matchups, home, away):
    #for round in list(matchups.values()):
    for i in range(1,5):
        round = matchups.get(str(i),[])
        for matchup in round:
            if matchup['home']['team']['id'] == int(home) and matchup['away']['team']['id'] == int(away):
                return matchup
    return None

def calculate_pts_old(player_id , preds, matchups):
    pts = 0
    results = calculate_results(player_id , preds, matchups)
    for result in results:
        if result['has_winner']:
            pts = pts + 5
            pts = pts + int(result['winner']['divisionRank'])
            if result['has_games']:
                pts = pts + 10

    return pts

def calculate_pts(player_id , preds, matchups):
    pts = 0
    results = calculate_results(player_id , preds, matchups)
    for result in results:
        if result['has_winner']:
            pts = pts + 10
            pts = pts + int(result['winner']['divisionRank'])
            if result['has_games']:
                pts = pts + 5

    return pts

def calculate_victories(player_id , preds, matchups):
    pts = {'winner_count': 0, 'games_count': 0}
    results = calculate_results(player_id , preds, matchups)
    for result in results:
        if result['has_winner']:
            pts['winner_count'] = pts['winner_count']  + 1
            if result['has_games']:
                pts['games_count'] = pts['games_count']  + 1
    return pts

def calculate_results(player_id , preds, matchups):
    results = []
    for prediction in preds:
        home = prediction['home']
        away = prediction['away']
        winner = prediction['winner']
        games = prediction['games']
        matchup = get_matchup(matchups, home, away)
        res = {'prediction': prediction, 'has_winner': False, 'has_games': False, 'winner':{}, 'games':0}
        if 'result' in matchup:
            result = matchup['result']
            match_winner = ''
            if result['home_win'] == 4:
                match_winner = home
                match_winner_info = matchup['home']
                winner_rank = int(matchup['home']['divisionRank'])
            elif result['away_win'] == 4:
                match_winner = away
                match_winner_info = matchup['away']
                winner_rank = int(matchup['away']['divisionRank'])
            match_games = int(result['home_win']) + int(result['away_win'])
            if match_winner != '':
                res['winner'] = match_winner_info
                res['games'] = match_games
                if match_winner == winner:
                    res['has_winner'] = True
                    if match_games == games:
                        res['has_games'] = True
            results.append(res)
    return results

def filter_predictions(preds, matchups):
    results = []
    for pred in preds:
        home = pred['home']
        away = pred['away']
        matchup = get_matchup(matchups, home, away)
        if matchups_store.is_matchup_started(matchup):
            results.append(pred)
    return results

def get(player_id, year):
    result=[]
    m = matchups_store.get_matchups(year)
    preds = predictions.get_all(year)
    for player in players.get_all_admin():
        player_preds = get_player_prediction(player['id'], preds)
        if len(player_preds) > 0:
            pts = calculate_pts(player['id'], get_player_prediction(player['id'], preds), m)
            oldpts = calculate_pts_old(player['id'], get_player_prediction(player['id'], preds), m)
            victories = calculate_victories(player['id'], get_player_prediction(player['id'], preds), m)
            if player['id'] != player_id:
                player_preds = filter_predictions(player_preds, m)
            result.append({'player':player['name'], 'pts':pts, 'oldpts':oldpts, 'predictions':player_preds, 'victories':victories})
    return result
