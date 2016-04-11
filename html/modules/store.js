class Store {
        constructor(server, year) {
                if(server == undefined)
                        server = '';
                if(year == undefined)
                        year = 2015;
                this.year = year;
                this.server = server;
                this.matchups = {};
                this.predictions = [];
                this.winners = [];
                this.currentround = 0;
        }

        getWinner(player){
                for (var winner of this.winners){
                        if(winner.player == player)
                                return winner.winner;
                }
                return null;
        }

        setWinner(player, winner, success, error){
                this.post(String(this.year) + "/winners",
                        {'player':player, 'winner':winner},
                        success,
                        error);
        }

        getPredictions(player, round){
                if (round == undefined)
                        round = this.currentround;
                var results = [];
                for (var matchup of this.matchups[round]){
                        var home = matchup.home.team.id;
                        var away = matchup.away.team.id;
                        var prediction = this.getPrediction(player, round, home, away);
                        if (prediction == null)
                                prediction = {'player':player, 'round':round, 'home':home, 'away':away, 'winner':0, 'games':4};
                        results.push(prediction);
                }
                return results;
        }

        getPrediction(player, round, home, away){
                for (var prediction of this.predictions){
                        if(prediction.player == player &&
                           prediction.round == round &&
                           prediction.home == home &&
                           prediction.away == away)
                                return prediction;
                }
                return null;
        }

        setPrediction(player, round, home, away, winner, games, success, error ){
                var prediction = {'player':player, 'round':round, 'home':home, 'away':away, 'winner':winner, 'games':games};
                this.post(String(this.year) + "/predictions",
                        prediction,
                        success,
                        error);
        }

        getTeams(){
                var results = [];
                for (var matchup of this.matchups[1]){
                        var home = matchup.home;
                        var away = matchup.away;
                        results.push(home);
                        results.push(away);
                }
                return results;
        }

        getTeam(id){
                var teams = this.getTeams();
                for (var team of teams){
                        if(team.team.id == id)
                                return team;
                }
                return null;
        }

        post(verb, data, success, error){
                $.ajax({
                type: 'POST',
                url: this.server +"/nhlplayoffs/api/v2.0/" + verb,
                data: JSON.stringify (data),
                success: success,
                error: error,
                contentType: "application/json",
                dataType: 'json'
                });
        }

        get(verb, success, error){
                $.ajax({
                type: 'GET',
                url: this.server +"/nhlplayoffs/api/v2.0/" + verb,
                success: success,
                error: error,
                contentType: "application/json",
                dataType: 'json'
                });
        }

        load(success, error){

                this.get(String(this.year) + "/data",
                        function(data) {
                                this.matchups = data.matchups;
                                this.currentround = data.current_round;
                                this.get(String(this.year) + "/predictions",
                                        function(data) {
                                                this.predictions = data.predictions;
                                                this.get(String(this.year) + "/winners",
                                                        function(data) {
                                                                this.winners = data.winners;
                                                                success();
                                                        }.bind(this),
                                                        error);
                                        }.bind(this),
                                        error);
                        }.bind(this),
                        error);
        }
}

module.exports = Store;
