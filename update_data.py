#!/usr/bin/python
from flask import Flask, jsonify, abort, request, send_from_directory, redirect, url_for
import json
import requests

app = Flask(__name__, static_url_path='')

year = 2015
data = {"matchups":{},
       "current_round":0}

def get_teams_stats():
    teams = requests.get('http://www.nhl.com/stats/rest/grouped/teams/season/teamsummary?cayenneExp=seasonId=20152016%20and%20gameTypeId=2')
    return teams.json()['data']

def get_players():
    players = requests.get('http://www.nhl.com/stats/rest/grouped/skaters/season/skatersummary?cayenneExp=seasonId=20152016%20and%20gameTypeId=2')
    return players.json()['data']

#utils ======================================
def print_matchups(matchups):
    for match in matchups:
        print(match['home']['team']['name'],match['home']['leagueRank'], match['away']['team']['name'],match['away']['leagueRank'])

def get_matchup_winner(matchup):
    if int(matchup['result']['home_win']) == 4:
        return matchup['home']
    else:
        return matchup['away']

def create_matchup(t1,t2):
    if int(t1['leagueRank']) <  int(t2['leagueRank']):
        return {'home':t1, 'away':t2}
    else:
        return {'home':t2, 'away':t1}

def get_conference_matchups(matchups, conference):
    matchs = []
    for match in matchups:
        conf = match['home']['conference']['name']
        if conf == conference:
            matchs.append(match)
    return matchs

def get_division_matchups(matchups, division):
    matchs = []
    for match in matchups:
        div = match['home']['division']['name']
        if div == division:
            matchs.append(match)
    return matchs

#teams ======================================
def get_teams(year = 2015):
    ystr = str(year) + str(year+1)
    url = 'https://statsapi.web.nhl.com/api/v1/standings?season=' + ystr
    print(url)
    standings = requests.get(url).json()
    teams = []
    for record in standings["records"]:
        for team in record['teamRecords']:
            team['conference'] = record['conference']
            team['division'] = record['division']
            teams.append(team)

    return teams

#standings ==================================
def get_standings(teams):
    standings = {'Eastern':{'Atlantic':[], 'Metropolitan':[], 'teams':[]},
                 'Western':{'Central':[], 'Pacific':[], 'teams':[]},
                 'teams':[]}

    league = sorted(teams, key=lambda k: int(k['divisionRank']))
    for team in league:
        standings['teams'].append(team)
        standings[team['conference']['name']]['teams'].append(team)
        standings[team['conference']['name']][team['division']['name']].append(team)
        #print(team['divisionRank'],team['conferenceRank'], team['conference']['name'],team['team']['name'])
    standings['teams'] = sorted(standings['teams'], key=lambda k: int(k['leagueRank']))

    standings['Eastern']['teams'] = sorted(standings['Eastern']['teams'], key=lambda k: int(k['conferenceRank']))
    standings['Western']['teams'] = sorted(standings['Western']['teams'], key=lambda k: int(k['conferenceRank']))

    standings['Eastern']['Atlantic'] = sorted(standings['Eastern']['Atlantic'], key=lambda k: int(k['divisionRank']))
    standings['Eastern']['Metropolitan'] = sorted(standings['Eastern']['Metropolitan'], key=lambda k: int(k['divisionRank']))
    standings['Western']['Central'] = sorted(standings['Western']['Central'], key=lambda k: int(k['divisionRank']))
    standings['Western']['Pacific'] = sorted(standings['Western']['Pacific'], key=lambda k: int(k['divisionRank']))

    return standings

#schedules ==================================
def get_schedule(team, year=2014):
    url = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate=' + str(year) + '-10-01&endDate=' + str(year+1) + '-06-29&expand=schedule.teams,schedule.linescore,schedule.broadcasts,schedule.ticket,schedule.game.content.media.epg&leaderCategories=&site=en_nhlCA&teamId=' + str(team)
    team_schedule = requests.get(url)
    return team_schedule.json()

def get_playoff_schedule(team, year=2014):
    url = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate=' + str(year+1) + '-04-01&endDate=' + str(year+1) + '-06-29&expand=schedule.teams,&site=en_nhlCA&teamId=' + str(team)
    team_schedule = requests.get(url)
    return team_schedule.json()

#matchups ====================================
def get_matchup_result(match):
    result = {}
    home_id = match['home']['team']['id']
    away_id = match['away']['team']['id']
    s = get_playoff_schedule(int(home_id), 2015)
    home_win = 0
    away_win = 0
    for date in s['dates']:
        game = date['games'][0]
        game_home_id = game['teams']['home']['team']['id']
        game_away_id = game['teams']['away']['team']['id']
        if game['gameType'] == 'P':
            if game_home_id == away_id or game_away_id == away_id:
                if game_home_id == away_id: #reverse
                    away_score = game['teams']['home']['score']
                    home_score = game['teams']['away']['score']
                else:
                    away_score = game['teams']['away']['score']
                    home_score = game['teams']['home']['score']
                if home_score > away_score:
                    home_win = home_win + 1
                else:
                    away_win = away_win + 1
                #print(match['home']['team']['name'], home_score, match['away']['team']['name'], away_score)
                #print(game['teams']['home']['team']['name'],game['teams']['home']['score'],match['away']['team']['name'],game['teams']['away']['score'])
    result['home_win'] = home_win
    result['away_win'] = away_win
    return result

def get_round1_matchups(year):
    teams = get_teams(year)
    standings = get_standings(teams)
    ealeader = standings['Eastern']['Atlantic'][0]
    emleader = standings['Eastern']['Metropolitan'][0]
    wcleader = standings['Western']['Central'][0]
    wpleader = standings['Western']['Pacific'][0]
    finished = True

    for team in teams:
        remaining = 82 - team['gamesPlayed']
        if remaining > 0:
            finished = False

    for team in standings['Eastern']['teams']:
        if int(team['wildCardRank']) == 1:
            e1wild = team
        if int(team['wildCardRank']) == 2:
            e2wild = team

    for team in standings['Western']['teams']:
        if int(team['wildCardRank']) == 1:
            w1wild = team
        if int(team['wildCardRank']) == 2:
            w2wild = team
    matchups = []
    if int(ealeader['conferenceRank']) < int(emleader['conferenceRank']):
        matchups.append({'home':ealeader, 'away':e2wild})
        matchups.append({'home':standings['Eastern']['Atlantic'][1], 'away':standings['Eastern']['Atlantic'][2]})
        matchups.append({'home':emleader, 'away':e1wild})
        matchups.append({'home':standings['Eastern']['Metropolitan'][1], 'away':standings['Eastern']['Metropolitan'][2]})
    elif int(ealeader['conferenceRank']) > int(emleader['conferenceRank']):
        matchups.append({'home':emleader, 'away':e2wild})
        matchups.append({'home':standings['Eastern']['Metropolitan'][1], 'away':standings['Eastern']['Metropolitan'][2]})
        matchups.append({'home':ealeader, 'away':e1wild})
        matchups.append({'home':standings['Eastern']['Atlantic'][1], 'away':standings['Eastern']['Atlantic'][2]})

    if int(wcleader['conferenceRank']) < int(wpleader['conferenceRank']):
        matchups.append({'home':wcleader, 'away':w2wild})
        matchups.append({'home':standings['Western']['Central'][1], 'away':standings['Western']['Central'][2]})
        matchups.append({'home':wpleader, 'away':w1wild})
        matchups.append({'home':standings['Western']['Pacific'][1], 'away':standings['Western']['Pacific'][2]})
    elif int(wcleader['conferenceRank']) > int(wpleader['conferenceRank']):
        matchups.append({'home':wpleader, 'away':w2wild})
        matchups.append({'home':standings['Western']['Pacific'][1], 'away':standings['Western']['Pacific'][2]})
        matchups.append({'home':wcleader, 'away':w1wild})
        matchups.append({'home':standings['Western']['Central'][1], 'away':standings['Western']['Central'][2]})
    return matchups, finished

def get_round2_matchups(round1_matchup):
    am = get_division_matchups(round1_matchup,"Atlantic")
    mm = get_division_matchups(round1_matchup,"Metropolitan")
    pm = get_division_matchups(round1_matchup,"Pacific")
    cm = get_division_matchups(round1_matchup,"Central")
    matchups = []
    matchups.append(create_matchup(get_matchup_winner(am[0]), get_matchup_winner(am[1])))
    matchups.append(create_matchup(get_matchup_winner(mm[0]), get_matchup_winner(mm[1])))
    matchups.append(create_matchup(get_matchup_winner(pm[0]), get_matchup_winner(pm[1])))
    matchups.append(create_matchup(get_matchup_winner(cm[0]), get_matchup_winner(cm[1])))
    return matchups

def get_round3_matchups(round2_matchup):
    am = get_division_matchups(round2_matchup,"Atlantic")
    mm = get_division_matchups(round2_matchup,"Metropolitan")
    pm = get_division_matchups(round2_matchup,"Pacific")
    cm = get_division_matchups(round2_matchup,"Central")
    matchups = []
    matchups.append(create_matchup(get_matchup_winner(am[0]), get_matchup_winner(mm[0])))
    matchups.append(create_matchup(get_matchup_winner(pm[0]), get_matchup_winner(cm[0])))
    return matchups

def get_round4_matchups(round3_matchup):
    em = get_conference_matchups(round3_matchup,"Eastern")
    wm = get_conference_matchups(round3_matchup,"Western")
    matchups = []
    matchups.append(create_matchup(get_matchup_winner(em[0]), get_matchup_winner(wm[0])))
    return matchups

def update_matchup(matchups):
    finished = True
    for match in matchups:
        result = get_matchup_result(match, year)
        match['result'] = result
        if result['home_win'] != 4 and  result['away_win'] != 4:
            finished = False
    return finished

def update():
    #Look which round we are in
    if data['current_round'] == 0:
        matchups, finished = get_round1_matchups(year)
        if finished:
            data['matchups'][1] = matchups
            print_matchups(data['matchups'][1])
            data['current_round'] = 1
        else:
            print('Season not finished')
            print_matchups(matchups)
    elif data['current_round'] == 1:
        #Get round 1 results
        finished = update_matchup(data['matchups'][1])
        if finished:
            data['matchups'][2] = get_round2_matchups(data['matchups'][1])
            print_matchups(data['matchups'][2])
            data['current_round'] = 2
    elif data['current_round'] == 2:
        finished = update_matchup(data['matchups'][2])
        if finished:
            data['matchups'][3] = get_round3_matchups(data['matchups'][2])
            print_matchups(data['matchups'][3])
            data['current_round'] = 3
    elif data['current_round'] == 3:
        finished = update_matchup(data['matchups'][3])
        if finished:
            data['matchups'][4] = get_round4_matchups(data['matchups'][3])
            print_matchups(data['matchups'][4])
            data['current_round'] = 4
    elif data['current_round'] == 4:
        finished = update_matchup(data['matchups'][4])
        if finished:
            winner = get_matchup_winner(data['matchups'][4][0])
            print('Winner:', winner['team']['name'])

teams = get_teams()
players = get_players()

@app.route('/html/<path:path>')
def send_js(path):
    return send_from_directory('html', path)

@app.route('/')
def root():
    html = ""
    for team in teams:
        id = team['id']
        img = "<img style='width: 100px;' src='https://www-league.nhlstatic.com/builds/site-core/284dc4ec70e4bee8802842e5e700157f45660a48_1457473228/images/team/logo/current/" + str(id) +"_dark.svg'>"
        html = html + img
    return html
    #return "<img src='http://cdn.nhle.com/nhl/images/logos/teams/"+ team.lower() + "_logo.svgz'>" + team;
    #return redirect('/html/nhlplayoffs.html')

if __name__ == '__main__':
    update()
    #app.run(debug=True,host='0.0.0.0', port=5000)
