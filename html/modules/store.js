class Store {
        constructor(server, year) {
                if(server == undefined)
                        server = '';
                if(year == undefined)
                        year = 2016;
                this.year = year;
                this.server = server;
                this.matchups = {};
                this.predictions = [];
                this.winners = [];
                this.currentround = 0;
                this.results = [];
        }

        display() {
             var nb_round = 4;
             var width = (nb_round * 2) - 1;
             var heigh = Math.pow(2,(nb_round-1)) -1;
             var display = [];
             for(var y=0;y<heigh;y++) {
                display[y] = [];
               for(var x=0;x<width;x++) {
                  display[y][x] = '';
               }
            }
            function walk_matchup_tree(root, x, y, dx){
                display[x][y] = root.id;
                if (root.left != null)
                  walk_matchup_tree(root.left, x+dx, y-(root.round-1), dx);
                if (root.right != null)
                  walk_matchup_tree(root.right, x+dx, y+(root.round-1), dx);
            }
            if (this.matchups.w == undefined)
                return;
            display[3][2] = 'sc';
            walk_matchup_tree(this.matchups.w, 2, 3, -1);
            walk_matchup_tree(this.matchups.e, 4, 3, 1);
            for(var y=0;y<heigh;y++) {
               var line = "";
              for(var x=0;x<width;x++) {
                 var id = display[x][y];
                 var cell = "";
                 if(id != ''){
                    var matchup = this.matchups[id];
                    if (matchup.home == 0) {
                       cell = id;
                       cell += " ".repeat(20 - cell.length);
                    } else {
                       var home = this.teams[matchup.home].info.abbreviation;
                       var away = '?';
                       if (matchup.away != 0)
                           away = this.teams[matchup.away].info.abbreviation;
                       cell = home + "-" + matchup.result.home_win + " vs " + matchup.result.away_win + "-"+ away;
                     cell += " ".repeat(20 - cell.length);
                    }
                 }
                 else{
                    cell += " ".repeat(20);
                 }
                 line +=  cell;

              }
              console.debug(line);
           }
        }

        buildMatchupTree(){
          for(var m in this.matchups){
             var matchup = this.matchups[m];
             if(matchup.next != "")
               matchup.next = this.matchups[matchup.next];
             if(matchup.left != "")
               matchup.left = this.matchups[matchup.left];
             if(matchup.right != "")
               matchup.right = this.matchups[matchup.right];}
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
                var matchups = this.getMatchups(0);
                matchups.sort(function(a, b){return b.round - a.round;});
                for (var matchup of matchups){
                        var home = matchup.home;
                        var away = matchup.away;
                        if(home != 0 && away != 0) {
                           var matchupRound = matchup.round;
                           var prediction = this.getPrediction(player, matchupRound, home, away);
                           if (prediction == null){
                                   prediction = {'player':player, 'round':matchupRound, 'home':home, 'away':away, 'winner':0, 'games':4};
                           }
                           results.push(prediction);
                        }
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
                for(var matchup of this.getMatchups(round)){
                        if(matchup.home == home && matchup.away == away)
                                return matchup;
                }
                return null;
        }

        getMatchups(round){
                var ms = []
                for (var key in this.matchups){
                    var matchup = this.matchups[key]
                    if (matchup.round == round || round == 0)
                        ms.push(matchup);
                }
                return ms;
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
                                        result.winner = matchup.home;
                                else if(matchup.result.home_win < matchup.result.away_win)
                                        result.winner = matchup.away;
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
                for (var matchup of this.getMatchups(round)){
                        if(this.isMatchupStarted(matchup))
                                return true;
                }
                return false;
        }

        getTeams(){
               //Look to filter teams not in playoff!!!!
               var teams = [];
               for(var t in this.teams){
                  teams.push(this.teams[t]);
               }
               return teams;
        }

        getTeam(id){
                var teams = this.getTeams();
                for (var team of teams){
                        if(team.info.id == id)
                                return team;
                }
                return null;
        }

        post(verb, data, success, error, version='v2.0'){
                $.ajax({
                type: 'POST',
                url: this.server +"/nhlplayoffs/api/"+ version +"/" + verb,
                data: JSON.stringify (data),
                success: success,
                error: error,
                contentType: "application/json",
                dataType: 'json'
                });
        }

        get(verb, success, error, version='v2.0'){
                $.ajax({
                type: 'GET',
                url: this.server +"/nhlplayoffs/api/" + version + "/" + verb,
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
                                this.teams = data.teams;
                                this.buildMatchupTree();
                                this.display();
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
                        error, "v3.0");
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
