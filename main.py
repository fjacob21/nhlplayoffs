#!/usr/bin/python
from flask import Flask, jsonify, abort, request, send_from_directory, redirect
import matchups
import matchupsv2
import predictions
import players
import postgres_store
from data import Data

_db = postgres_store.get_default()
application = Flask(__name__, static_url_path='')

@application.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@application.route('/nhlplayoffs/api/v2.0/teams', methods=['GET'])
def get_all_teamss():
    return jsonify({'teams': matchupsv2.get_teams()})

@application.route('/nhlplayoffs/api/v2.0/players', methods=['GET'])
def get_all_players():
    _data = Data()
    ps = _data.get_players()
    for p in ps:
        del p['id']
    return jsonify({'players': ps})

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
    p = players.get(name)
    return jsonify({'user':result, 'info': p})

@application.route('/nhlplayoffs/api/v2.0/players/<string:player>', methods=['GET'])
def get_player(player):
    p = players.get(player)
    if p is None:
        abort(400)
    return jsonify(p)

@application.route('/nhlplayoffs/api/v2.0/players/<string:player>/reset', methods=['POST'])
def reset_player(player):
    if not request.json:
        print('not json')
        abort(400)

    if ("root_psw" not in request.json or
        "new_psw" not in request.json):
        abort(400)
    root_psw = request.json["root_psw"]
    new_psw = request.json["new_psw"]
    result = players.change_psw(player, '', new_psw, players.root_access(root_psw))
    return jsonify({"result":result})

@application.route('/nhlplayoffs/api/v2.0/players/<string:player>/chpsw', methods=['POST'])
def change_psw_player(player):
    if not request.json:
        print('not json')
        abort(400)

    if ("old_psw" not in request.json or
        "new_psw" not in request.json):
        abort(400)
    old_psw = request.json["old_psw"]
    new_psw = request.json["new_psw"]
    result = players.change_psw(player, old_psw, new_psw)
    return jsonify({"result":result})

@application.route('/nhlplayoffs/api/v2.0/players/<string:player>', methods=['PUT'])
def update_player(player):
    if not request.json:
        abort(400)

    if "email" in request.json:
        email = request.json["email"]

    result = players.change_email(player, email)
    return jsonify({'result': True})

@application.route('/nhlplayoffs/api/v2.0/players/<string:player>', methods=['DELETE'])
def delete_player(player):
    if not request.json:
        print('not json')
        abort(400)

    if ("root_psw" not in request.json):
        print('No root psw')
        abort(400)

    root_psw = request.json["root_psw"]

    if not players.root_access(root_psw):
        print('Invalid root psw')
        abort(403)

    print('Remove player', player)
    result = players.remove(player)
    return jsonify({"result":result})

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
    p = players.get(player)
    if result is None:
        abort(400)
    return jsonify({'user':result, 'info': p})

@application.route('/nhlplayoffs/api/v2.0/<int:year>/data', methods=['GET'])
def get_data(year):
    return jsonify(matchups.get(year))

@application.route('/nhlplayoffs/api/v2.0/<int:year>/data', methods=['POST'])
def update_data(year):
    if not request.json:
        abort(400)
    matchups.update(year,request.json)
    return ''

@application.route('/nhlplayoffs/api/v3.0/<int:year>/data', methods=['GET'])
def get_datav3(year):
    return jsonify(matchupsv2.get(year))

@application.route('/nhlplayoffs/api/v3.0/<int:year>/data', methods=['POST'])
def update_datav3(year):
    if not request.json:
        abort(400)
    matchupsv2.update(year,request.json)
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

@application.route('/nhlplayoffs/api/v2.0/<int:year>/results', methods=['POST'])
def get_results(year):
    if not request.json:
        abort(400)

    if "player" not in request.json:
        abort(400)
    player = request.json["player"]

    _data = Data(player)
    r = _data.get_results(player, year)
    return jsonify({"results": r})

@application.route('/nhlplayoffs/api/v2.0/backup', methods=['POST'])
def backup():
    if not request.json:
        print('not json')
        abort(400)

    if "root_psw" not in request.json:
        abort(403)

    root_psw = request.json["root_psw"]
    if not players.root_access(root_psw):
        abort(403)

    return jsonify(_db.backup())

@application.route('/nhlplayoffs/api/v2.0/restore', methods=['POST'])
def restore():
    if not request.json:
        print('not json')
        abort(400)

    if ("root_psw" not in request.json or
        "data" not in request.json):
        abort(403)

    root_psw = request.json["root_psw"]
    if not players.root_access(root_psw):
        abort(403)

    data = request.json["data"]
    return jsonify({'result':_db.restore_backup(data)})

@application.route('/html/<path:path>')
def send_js(path):
    return send_from_directory('html', path)

@application.route('/')
def root():
    return redirect('/html/index.html')

if __name__ == '__main__':
    application.run(debug=True,host='0.0.0.0', port=5000)
