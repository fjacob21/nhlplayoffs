# Results management module
#
import matchups
import players
import predictions

def get_player_prediction(player_id, preds):

    result=[]
    for prediction in preds:
        if prediction['player'] == player_id:
            #p = prediction.copy()
            #del p['player']
            result.append(prediction)
    return result

def get_matchup(matchups, home, away):
    #for round in list(matchups.values()):
    for i in range(1,5):
        round = matchups.get(str(i),[])
        for matchup in round:
            if matchup['home']['team']['id'] == int(home) and matchup['away']['team']['id'] == int(away):
                return matchup
    return None

def calculate_pts(player_id, preds, matchups):
    #preds = get_player_prediction(player_id, year)
    pts=0
    for prediction in preds:
        home = prediction['home']
        away = prediction['away']
        winner = prediction['winner']
        games = prediction['games']
        matchup = get_matchup(matchups, home, away)
        if 'result' in matchup:
            result = matchup['result']
            match_winner = ''
            if result['home_win'] == 4:
                match_winner = home
                winner_rank = int(matchup['home']['divisionRank'])
            elif result['away_win'] == 4:
                match_winner = away
                winner_rank = int(matchup['away']['divisionRank'])
            match_games = int(result['home_win']) + int(result['away_win'])
            if match_winner != '':
                if match_winner == winner:
                    #print(winner_rank,matchup['home']['team']['name'],matchup['away']['team']['name'])
                    pts = pts + 10
                    pts = pts + winner_rank
                    if match_games == games:
                        pts = pts + 5
    return pts

def calculate_pts_old(player_id, year):
    preds = get_player_prediction(player_id, year)
    pts=0
    for prediction in preds:
        home = prediction['home']
        away = prediction['away']
        winner = prediction['winner']
        games = prediction['games']
        matchup = matchups.get_matchup(year, home, away)
        if 'result' in matchup:
            result = matchup['result']
            match_winner = ''
            if result['home_win'] == 4:
                match_winner = home
                winner_rank = int(matchup['home']['divisionRank'])
            elif result['away_win'] == 4:
                match_winner = away
                winner_rank = int(matchup['away']['divisionRank'])
            match_games = int(result['home_win']) + int(result['away_win'])
            if match_winner != '':
                if match_winner == winner:
                    #print(winner_rank,matchup['home']['team']['name'],matchup['away']['team']['name'])
                    pts = pts + 5
                    pts = pts + winner_rank
                    if match_games == games:
                        pts = pts + 10
    return pts

def get(player_id, year):
    result=[]
    m = matchups.get_matchups(year)
    preds = predictions.get_all(year)
    for player in players.get_all_admin():
        pts = 0#calculate_pts(player['id'], get_player_prediction(player_id, preds), m)
        oldpts = 0#calculate_pts_old(player['id'], year)
        #preds = get_player_prediction(player['id'], year)
        result.append({'player':player['name'], 'pts':pts, 'oldpts':oldpts})
    return result
