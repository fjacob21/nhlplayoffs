#!flask/bin/python
from flask import Flask, jsonify, abort, request, send_from_directory, redirect, url_for
import json

app = Flask(__name__, static_url_path='')

#with open("data_2015.json") as data:
with open("data_2015.json") as data:
    data_2015=json.load(data)

playoffs_data={}
playoffs_data[2015] = data_2015

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

@app.route('/nhlplayoffs/api/v1.0/<int:year>/current_round', methods=['GET'])
def get_current_round(year):
    return jsonify({"current_round":playoffs_data[year]["current_round"]})

@app.route('/nhlplayoffs/api/v1.0/<int:year>/teams', methods=['GET'])
def get_teams(year):
    return jsonify({"teams":playoffs_data[year]["teams"]})

@app.route('/nhlplayoffs/api/v1.0/<int:year>/teams/<string:team_id>', methods=['GET'])
def get_team(year,team_id):
    team = [team for team in playoffs_data[year]["teams"] if team['id'] == team_id]
    return jsonify({"team":team[0]})

@app.route('/nhlplayoffs/api/v1.0/<int:year>/series', methods=['GET'])
def get_series(year):
    return jsonify({"series":playoffs_data[year]["series"]})

@app.route('/nhlplayoffs/api/v1.0/<int:year>/series/<int:series_id>', methods=['GET'])
def get_serie(year,series_id):
    serie = [serie for serie in playoffs_data[year]["serie"] if serie['id'] == series_id]
    return jsonify({"serie":serie[0]})

@app.route('/nhlplayoffs/api/v1.0/<int:year>/series', methods=['POST'])
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

@app.route('/nhlplayoffs/api/v1.0/<int:year>/predictions', methods=['GET'])
def get_predictions(year):
    return jsonify({"predictions":playoffs_data[year]["predictions"]})

@app.route('/nhlplayoffs/api/v1.0/<int:year>/predictions/<int:series_id>', methods=['GET'])
def get_prediction(year,series_id):
    prediction = [prediction for prediction in playoffs_data[year]["predictions"] if prediction['id'] == series_id]
    return jsonify({"prediction":prediction[0]})

@app.route('/nhlplayoffs/api/v1.0/<int:year>/predictions', methods=['POST'])
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

@app.route('/nhlplayoffs/api/v1.0/<int:year>/winner_predictions', methods=['GET'])
def get_winner_predictions(year):
    return jsonify({"winner_predictions":playoffs_data[year]["winner_predictions"]})

@app.route('/nhlplayoffs/api/v1.0/<int:year>/winner_predictions', methods=['POST'])
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

@app.route('/html/<path:path>')
def send_js(path):
    return send_from_directory('html', path)

@app.route('/')
def root():
    return redirect('/html/nhlplayoffs.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
