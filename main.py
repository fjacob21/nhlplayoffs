#!/usr/bin/python
from flask import Flask, jsonify, abort, request, send_from_directory, redirect, url_for
import json
import os
import urlparse
import matchups
import predictions
import players
from postgres_store import postgres_store

application = Flask(__name__, static_url_path='')
#db = postgres_store('dc7m5co1u7n7ka', 'vfumyroepkgfsd', 'AsRCUy1JTkf500s_2pfXZK9qwR', 'ec2-107-22-246-250.compute-1.amazonaws.com', 5432)
#db = postgres_store('dc7m5co1u7n7ka', 'vfumyroepkgfsd', 'AsRCUy1JTkf500s_2pfXZK9qwR', 'ec2-107-22-246-250.compute-1.amazonaws.com', 5432)
#with open("data_2015.json") as data:
data = '{"teams":[{"id":"nyr","name":"Rangers","rank":1,"division":"east"},{"id":"mtl", "name":"Canadiens", "rank":2, "division":"east"}, {"id":"tbl", "name":"Lightning", "rank":3, "division":"east"}, {"id":"wsh", "name":"Capitals", "rank":4, "division":"east"}, {"id":"nyi", "name":"Islanders", "rank":5, "division":"east"}, {"id":"pit", "name":"Penguins", "rank":8, "division":"east"}, {"id":"det", "name":"RedWings", "rank":6, "division":"east"}, {"id":"bos", "name":"Bruins", "rank":9, "division":"east"}, {"id":"ott", "name":"Senators", "rank":7, "division":"east"}, {"id":"ana", "name":"Ducks", "rank":1, "division":"west"}, {"id":"nsh", "name":"Predators", "rank":3, "division":"west"}, {"id":"stl", "name":"Blues", "rank":2, "division":"west"}, {"id":"chi", "name":"Blackhawks", "rank":4, "division":"west"}, {"id":"min", "name":"Wild", "rank":6, "division":"west"}, {"id":"van", "name":"Canucks", "rank":5, "division":"west"}, {"id":"wpg", "name":"Jets", "rank":7, "division":"west"}, {"id":"cgy", "name":"Flames", "rank":8, "division":"west"}, {"id":"lak", "name":"Kings", "rank":9, "division":"west"} ], "series":[{"home":"mtl", "visitor":"ott", "round":1, "home_win":0, "visitor_win":0}, {"home":"tbl", "visitor":"det", "round":1, "home_win":0, "visitor_win":0}, {"home":"nyr", "visitor":"pit", "round":1, "home_win":0, "visitor_win":0}, {"home":"wsh", "visitor":"nyi", "round":1, "home_win":0, "visitor_win":0}, {"home":"stl", "visitor":"min", "round":1, "home_win":0, "visitor_win":0}, {"home":"nsh", "visitor":"chi", "round":1, "home_win":0, "visitor_win":0}, {"home":"ana", "visitor":"wpg", "round":1, "home_win":0, "visitor_win":0}, {"home":"van", "visitor":"cgy", "round":1, "home_win":0, "visitor_win":0} ], "predictions":[], "current_round":1, "winner_predictions":[]}'

#with open("data_2016.json") as data:
data_2016=json.loads(data)

playoffs_data={}
playoffs_data[2016] = data_2016

def write_data_file(year):
    with open('data_' + str(year) + '.json', 'w') as outfile:
        json.dump(playoffs_data[year], outfile, indent=4, sort_keys=True)

def find_prediction(data, player, home, visitor):
    for prediction in data["predictions"]:
        if prediction["player"]==player and prediction["home"]==home and prediction["visitor"]==visitor:
            return prediction
    return None

def find_winner_prediction(data, player):
    for prediction in data["winner_predictions"]:
        if prediction["player"]==player:
            return prediction
    return None

def find_serie(data, home, visitor):
    for serie in data["series"]:
        if serie["home"]==home and serie["visitor"]==visitor:
            return serie
    return None

@application.route('/nhlplayoffs/api/v1.0/<int:year>/current_round', methods=['GET'])
def get_current_round(year):
    return jsonify({"current_round":playoffs_data[year]["current_round"]})

@application.route('/nhlplayoffs/api/v1.0/<int:year>/teams', methods=['GET'])
def get_teams(year):
    return jsonify({"teams":playoffs_data[year]["teams"]})

@application.route('/nhlplayoffs/api/v1.0/<int:year>/teams/<string:team_id>', methods=['GET'])
def get_team(year,team_id):
    team = [team for team in playoffs_data[year]["teams"] if team['id'] == team_id]
    return jsonify({"team":team[0]})

@application.route('/nhlplayoffs/api/v1.0/<int:year>/series', methods=['GET'])
def get_series(year):
    return jsonify({"series":playoffs_data[year]["series"]})

@application.route('/nhlplayoffs/api/v1.0/<int:year>/series/<int:series_id>', methods=['GET'])
def get_serie(year,series_id):
    serie = [serie for serie in playoffs_data[year]["serie"] if serie['id'] == series_id]
    return jsonify({"serie":serie[0]})

@application.route('/nhlplayoffs/api/v1.0/<int:year>/series', methods=['POST'])
def create_serie(year):
    if not request.json:
        abort(400)

    serie = find_serie(playoffs_data[year],request.json["home"],request.json["visitor"])

    if  serie == None:
        serie = {
            'home': request.json['home'],
            'visitor': request.json['visitor'],
            'round': request.json['round'],
            'home_win': request.json['home_win'],
            'visitor_win': request.json['visitor_win']
        }
        playoffs_data[year]["series"].append(serie)
    else:
        serie["home"] = request.json['home']
        serie["visitor"] = request.json['visitor']
        serie["round"] = request.json['round']
        serie["home_win"] = request.json['home_win']
        serie["visitor_win"] = request.json['visitor_win']

    write_data_file(year)

    return jsonify({'serie': serie, "result":"success"}), 201

@application.route('/nhlplayoffs/api/v1.0/<int:year>/predictions', methods=['GET'])
def get_predictions(year):
    return jsonify({"predictions":playoffs_data[year]["predictions"]})

@application.route('/nhlplayoffs/api/v1.0/<int:year>/predictions/<int:series_id>', methods=['GET'])
def get_prediction(year,series_id):
    prediction = [prediction for prediction in playoffs_data[year]["predictions"] if prediction['id'] == series_id]
    return jsonify({"prediction":prediction[0]})

@application.route('/nhlplayoffs/api/v1.0/<int:year>/predictions', methods=['POST'])
def create_prediction(year):
    if not request.json:
        abort(400)

    prediction = find_prediction(playoffs_data[year],request.json["player"],request.json["home"],request.json["visitor"])

    if  prediction == None:
        prediction = {
            'player': request.json['player'],
            'home': request.json['home'],
            'visitor': request.json['visitor'],
            'win_team': request.json['win_team'],
            'win_games': request.json['win_games']
        }
        playoffs_data[year]["predictions"].append(prediction)
    else:
        prediction["player"] = request.json['player']
        prediction["home"] = request.json['home']
        prediction["visitor"] = request.json['visitor']
        prediction["win_team"] = request.json['win_team']
        prediction["win_games"] = request.json['win_games']

    write_data_file(year)

    return jsonify({'prediction': prediction, "result":"success"}), 201

@application.route('/nhlplayoffs/api/v1.0/<int:year>/winner_predictions', methods=['GET'])
def get_winner_predictions(year):
    return jsonify({"winner_predictions":playoffs_data[year]["winner_predictions"]})

@application.route('/nhlplayoffs/api/v1.0/<int:year>/winner_predictions', methods=['POST'])
def set_winner_predictions(year):
    if not request.json:
        abort(400)

    winner_prediction = find_winner_prediction(playoffs_data[year],request.json["player"])

    if  winner_prediction == None:
        winner_prediction = {
            'player': request.json['player'],
            'winner': request.json['winner'],
        }
        playoffs_data[year]["winner_predictions"].append(winner_prediction)
    else:
        winner_prediction["player"] = request.json['player']
        winner_prediction["winner"] = request.json['winner']

    write_data_file(year)

    return jsonify({'winner_prediction': winner_prediction, "result":"success"}), 201

@application.route('/nhlplayoffs/api/v2.0/players', methods=['GET'])
def get_all_players():
    return jsonify({'players':players.get_all()})

@application.route('/nhlplayoffs/api/v2.0/players', methods=['POST'])
def add_player():
    if not request.json:
        abort(400)

    if "name" not in request.json or "psw" not in request.json:
        abort(400)

    name = request.json["name"]
    psw = request.json["psw"]
    email = ''
    if "email" in request.json:
        email = request.json["email"]
    admin = False
    if "admin" in request.json:
        admin = request.json["admin"]
    if not players.add(name, psw, email, admin):
        abort(400)
    result = players.login(name, psw)
    return jsonify({'user':result})

@application.route('/nhlplayoffs/api/v2.0/players/<string:player>', methods=['GET'])
def get_player(player):
    p = players.get(player)
    if p is None:
        abort(400)
    return jsonify(p)

@application.route('/nhlplayoffs/api/v2.0/players/<string:player>', methods=['PUT'])
def update_player(player):
    if not request.json:
        abort(400)
    return ""

@application.route('/nhlplayoffs/api/v2.0/players/<string:player>', methods=['DELETE'])
def delete_player(player):
    if not players.remove(player):
        abort(400)

    return ""

@application.route('/nhlplayoffs/api/v2.0/players/<string:player>/login', methods=['POST'])
def login_player(player):
    if not request.json:
        print('not json')
        abort(400)

    if "psw" not in request.json:
        print('no psw')
        abort(400)
    psw = request.json["psw"]
    result = players.login(player, psw)
    if result is None:
        abort(400)
    return jsonify({'user':result})

@application.route('/nhlplayoffs/api/v2.0/<int:year>/data', methods=['GET'])
def get_data(year):
    return jsonify(matchups.get(year))

@application.route('/nhlplayoffs/api/v2.0/<int:year>/data', methods=['POST'])
def update_data(year):
    if not request.json:
        abort(400)
    matchups.update(year,request.json)
    return ''

@application.route('/nhlplayoffs/api/v2.0/<int:year>/currentround', methods=['GET'])
def get_current_roundv2(year):
    return jsonify({'current_round':matchups.get_current_round(year)})

@application.route('/nhlplayoffs/api/v2.0/<int:year>/matchups', methods=['GET'])
def get_matchups(year):
    return jsonify(matchups.get_matchups(year))


@application.route('/nhlplayoffs/api/v2.0/<int:year>/winners', methods=['GET'])
def get_winnersv2(year):
    p = predictions.get_winners(year)
    return jsonify({'winners':p})

@application.route('/nhlplayoffs/api/v2.0/<int:year>/winners', methods=['POST'])
def add_winner(year):
    if not request.json:
        abort(400)

    if ("player" not in request.json or
       "winner" not in request.json):
        abort(400)
    player = request.json["player"]
    winner = request.json["winner"]

    if not predictions.add_winner(player, year, winner):
        abort(400)
    return jsonify({"result":True})

@application.route('/nhlplayoffs/api/v2.0/<int:year>/predictions', methods=['GET'])
def get_predictionsv2(year):
    p = predictions.get_all(year)
    return jsonify({'predictions':p})

@application.route('/nhlplayoffs/api/v2.0/<int:year>/predictions', methods=['POST'])
def add_prediction(year):
    if not request.json:
        abort(400)

    print(request.json)
    if ("player" not in request.json or
       "round" not in request.json or
       "home" not in request.json or
       "away" not in request.json or
       "winner" not in request.json or
       "games" not in request.json):
        abort(400)
    player = request.json["player"]
    round = request.json["round"]
    home = request.json["home"]
    away = request.json["away"]
    winner = request.json["winner"]
    games = request.json["games"]

    if not predictions.add(player, year, round, home, away, winner, games):
        abort(400)
    return jsonify({"result":True})

@application.route('/html/<path:path>')
def send_js(path):
    return send_from_directory('html', path)

@application.route('/')
def root():
    return redirect('/html/index.html')

#if __name__ == '__main__':
#application.run(debug=True,host='0.0.0.0', port=5000)
