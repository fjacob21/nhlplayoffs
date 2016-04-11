#!/usr/bin/python
from flask import Flask, jsonify, abort, request, send_from_directory, redirect, url_for
import json
import os
import urlparse
import matchups
import predictions
import players

application = Flask(__name__, static_url_path='')

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

if __name__ == '__main__':
    application.run(debug=True,host='0.0.0.0', port=5000)
