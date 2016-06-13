# Results management module
#
import matchupsv2 as matchups_store
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

def get_winner(player, winners):
    for winner in winners:
        if winner['player'] == player:
            return int(winner['winner'])
    return None

def get_matchup(matchups, home, away):
    for matchup in list(matchups.values()):
        if matchup['home'] == int(home) and matchup['away'] == int(away):
            return matchup
    return None

def get_final_winner(year, teams):
    matchups = matchups_store.get_matchups(year, 4)
    result = calculate_matchup_result(matchups[0], teams)
    if result['winner'] != 0:
        return result['winner']
    return 0

def calculate_pts_old(player_id , preds, matchups, teams, winner, final_winner):
    pts = 0
    results = calculate_results(player_id , preds, matchups, teams)
    for result in results:
        if result['has_winner']:
            pts = pts + 5
            pts = pts + int(result['winner']['conferenceRank'])
            if result['has_games']:
                pts = pts + 10
    if winner == final_winner:
            pts = pts + 50
    return pts

def calculate_pts(player_id , preds, matchups, teams, winner, final_winner):
    pts = 0
    results = calculate_results(player_id , preds, matchups, teams)
    for result in results:
        if result['has_winner']:
            pts = pts + 10
            pts = pts + int(result['winner']['conferenceRank'])
            if result['has_games']:
                pts = pts + 5
    if winner == final_winner:
            pts = pts + 50
    return pts

def calculate_victories(player_id , preds, matchups, teams):
    pts = {'winner_count': 0, 'games_count': 0}
    results = calculate_results(player_id , preds, matchups, teams)
    for result in results:
        if result['has_winner']:
            pts['winner_count'] = pts['winner_count']  + 1
            if result['has_games']:
                pts['games_count'] = pts['games_count']  + 1
    return pts

def calculate_matchup_result(matchup, teams):
    home = matchup['home']
    away = matchup['away']
    match_winner = 0
    match_winner_info = {}
    winner_rank = 0
    match_games = 0
    if 'result' in matchup:
        result = matchup['result']
        if result['home_win'] == 4:
            match_winner = home
            match_winner_info = teams[matchup['home']]['standings']
            winner_rank = int(teams[matchup['home']]['standings']['conferenceRank'])
        elif result['away_win'] == 4:
            match_winner = away
            match_winner_info = teams[matchup['away']]['standings']
            winner_rank = int(teams[matchup['away']]['standings']['conferenceRank'])
        match_games = int(result['home_win']) + int(result['away_win'])
    return {"winner":match_winner, "winner_info":match_winner_info, "winner_rank":winner_rank, "games":match_games}

def calculate_results(player_id , preds, matchups, teams):
    results = []
    for prediction in preds:
        home = prediction['home']
        away = prediction['away']
        winner = prediction['winner']
        games = prediction['games']
        matchup = get_matchup(matchups, home, away)
        res = {'prediction': prediction, 'has_winner': False, 'has_games': False, 'winner':{}, 'games':0}
        result = calculate_matchup_result(matchup, teams)
        if result['games'] != 0:
            if result['winner'] != 0:
                res['winner'] = result['winner_info']
                res['games'] = result['games']
                if winner == result['winner']:
                    res['has_winner'] = True
                    if games == result['games']:
                        res['has_games'] = True
            results.append(res)
        # if 'result' in matchup:
        #     result = matchup['result']
        #     match_winner = ''
        #     if result['home_win'] == 4:
        #         match_winner = home
        #         match_winner_info = teams[matchup['home']]['standings']
        #         winner_rank = int(teams[matchup['home']]['standings']['conferenceRank'])
        #     elif result['away_win'] == 4:
        #         match_winner = away
        #         match_winner_info = teams[matchup['away']]['standings']
        #         winner_rank = int(teams[matchup['away']]['standings']['conferenceRank'])
        #     match_games = int(result['home_win']) + int(result['away_win'])
        #     if match_winner != '':
        #         res['winner'] = match_winner_info
        #         res['games'] = match_games
        #         if match_winner == winner:
        #             res['has_winner'] = True
        #             if match_games == games:
        #                 res['has_games'] = True
        #     results.append(res)
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
    teams = matchups_store.get_teams(year)
    preds = predictions.get_all(year)
    final_winner = get_final_winner(year, teams)
    winners = predictions.get_winners(year)
    for player in players.get_all_admin():
        player_preds = get_player_prediction(player['id'], preds)
        winner = get_winner(player['id'], winners)
        if len(player_preds) > 0:
            pts = calculate_pts(player['id'], get_player_prediction(player['id'], preds), m, teams, winner, final_winner)
            oldpts = calculate_pts_old(player['id'], get_player_prediction(player['id'], preds), m, teams, winner, final_winner)
            victories = calculate_victories(player['id'], get_player_prediction(player['id'], preds), m, teams)
            winner = predictions.get_winner(player['id'], year)
            if winner is not None:
                winner = winner['winner']
            else:
                winner = 0
            if player['id'] != player_id:
                player_preds = filter_predictions(player_preds, m)
            result.append({'player':player['name'], 'pts':pts, 'oldpts':oldpts, 'winner':winner, 'predictions':player_preds, 'victories':victories})
    return result
