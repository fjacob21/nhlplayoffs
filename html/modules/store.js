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
                this.results = [];
        }

        getTeamImgUrl(team){
                return 'https://www-league.nhlstatic.com/builds/site-core/284dc4ec70e4bee8802842e5e700157f45660a48_1457473228/images/team/logo/current/' + team + '_dark.svg';
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

        getMatchup(home, away, round){
                for(var matchup of this.matchups[round]){
                        if(matchup.home.team.id == home && matchup.away.team.id == away)
                                return matchup;
                }
                return null;
        }

        getMatchups(round){
                return this.matchups[round];
        }

        getMatchupTime(matchup){
                if(matchup.start == undefined)
                        return null;
                var start  = new Date(matchup.start);
                var now = new Date(Date.now());
                var diff = start-now;
                var diffDay = Math.max(0, Math.floor((start-now)/(1000*60*60*24)));
                var diffHour = Math.max(0, Math.floor((start-now - (diffDay*(1000*60*60*24)))/(1000*60*60)));
                var diffMin = Math.max(0, Math.floor((start-now - (diffDay*(1000*60*60*24)) - (diffHour*(1000*60*60)))/(1000*60)));
                return {'days': diffDay, 'hours': diffHour, 'minutes': diffMin};
        }

        getMatchupResult(matchup){
                var result = {'winner': 0, 'games':0, 'isFinish':false};

                if(matchup.result != undefined){
                        result.games = matchup.result.home_win + matchup.result.away_win;

                        if(result.games > 0){
                                if(matchup.result.home_win > matchup.result.away_win)
                                        result.winner = matchup.home.team.id;
                                else if(matchup.result.home_win < matchup.result.away_win)
                                        result.winner = matchup.away.team.id;
                        }

                        if(matchup.result.home_win == 4 || matchup.result.away_win == 4)
                                result.isFinish = true;
                }
                return result;
        }

        isMatchupStarted(matchup){
                var time = this.getMatchupTime(matchup);
                if(time == null)
                        return false;
                if(time.days == 0 && time.hours == 0 && time.minutes == 0)
                        return true;
                return false;
        }

        isRountStarted(round){
                for (var matchup of this.matchups[round]){
                        if(this.isMatchupStarted(matchup))
                                return true;
                }
                return false;
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

        loadResults(player, success, error){
                var data = {'player':player};
                this.post(String(this.year) + "/results",
                        data,
                        function(data) {
                                this.results = data.results;
                                success();
                        }.bind(this),
                        error);
        }
}

module.exports = Store;
