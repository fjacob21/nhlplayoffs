function compare_predictions(a,b) {
        if(a.round<b.round)
                return -1;
        else if(a.round>b.round)
                return 1;
        else{
          if(a.home.division != b.home.division){
            if(a.home.division == "west")
              return -1;
            else
              return 1;
          }
          else {
            if (a.home.rank < b.home.rank)
               return -1;
            if (a.home.rank > b.home.rank)
              return 1;
            return 0;
          }
        }
}

function compare_players(a,b) {
  if(a.pts > b.pts)
      return -1;
  else if(a.pts < b.pts)
      return 1;
  else{
    if(a.name.toLowerCase() > b.name.toLowerCase())
      return 1;
    else
      return -1;
  }
}

function data(current_year){
        newobj = {

        year:current_year,
        round:0,
        series:[],
        team:[],
        predictions:[],
        winner_predictions:[],
        data_loaded:{teams:false, series:false, predictions:false, round:false, winner:false},
        predictions_table:[],
        players:[],
        onDataLoaded:null,

        is_data_loaded: function(){return (this.data_loaded.teams&&this.data_loaded.series&&this.data_loaded.predictions&&this.data_loaded.round&&this.data_loaded.winner);},

        call_data_loaded: function(){
                if(this.is_data_loaded())
                        if(this.onDataLoaded!=null)
                                this.onDataLoaded();},

        build_request_url: function(request){
                return "/nhlplayoffs/api/v1.0/" + this.year + "/"+request;
        },

        send_get_request: function(request, success){
                $.ajax({
                    url: this.build_request_url(request),
                    type: "GET",
                    dataType: "json",
                    success: success,
                    error: function (xhr, status, errorThrown) {
                        console.log("Error: " + errorThrown);
                        console.log("Status: " + status);
                        console.dir(xhr);
                    },
                    complete: function (xhr, status) {
                    }
                });
        },

        send_post_request: function(request, data){
                var result = $.ajax({
                    url: this.build_request_url(request),
                    type: "POST",
                    dataType: "json",
                    contentType: 'application/json; charset=utf-8',
                    data: JSON.stringify(data),
                    async: false
                });
                if(result.status != 201 )
                        return false;
                return true;
        },

        get_predictions: function(){
                var self=this;
                this.send_get_request("predictions", function(json){
                        self.data_loaded.predictions = true;
                        self.predictions = json.predictions;
                        self.call_data_loaded();});
        },
        set_prediction: function(player, home, visitor, win_team, win_games){
                var data ={"player":player, "home":home, "visitor":visitor, "win_team":win_team, "win_games":win_games};
                return this.send_post_request("predictions", data);
        },

        get_winner_predictions:function(){
                var self=this;
                this.send_get_request("winner_predictions", function(json){
                        self.data_loaded.winner = true;
                        self.winner_predictions = json.winner_predictions;
                        self.call_data_loaded();});
        },
        set_winner_predictions: function(player, winner){
                var data ={"player":player, "winner":winner};
                return this.send_post_request("winner_predictions", data);
        },

        get_teams:function(){
                var self=this;
                this.send_get_request("teams", function(json){
                        self.data_loaded.teams = true;
                        self.teams = json.teams;
                        self.call_data_loaded();});
        },

        get_current_round:function(){
                var self=this;
                this.send_get_request("current_round", function(json){
                        self.data_loaded.round = true;
                        self.round = json.current_round;
                        self.call_data_loaded();});
        },

        get_series:function(){
                var self=this;
                this.send_get_request("series", function(json){
                        self.data_loaded.series = true;
                        self.series = json.series;
                        self.call_data_loaded();});
        },
        set_series: function(round, home, visitor, home_wins, visitor_win){
                var data ={"round":round, "home":home, "visitor":visitor, "home_win":home_wins, "visitor_win":visitor_win};
                return this.send_post_request("series", data);
        },

        calculate_player_pts:function(player){
          var pts = 0;
          for (var i = 0; i < player.predictions.length; i++) {
            var prediction = player.predictions[i];
            var serie = this.find_serie(prediction.home, prediction.visitor);
            var winner = "";
            if(serie.home_win == 4)winner = serie.home;
            if(serie.visitor_win == 4)winner = serie.visitor;

            if(prediction.win_team == winner ) {
                pts+=5;
                if(parseInt(prediction.win_games) == (parseInt(serie.home_win)+parseInt(serie.visitor_win))) pts+=10;
            }
          }
          player.pts=pts;
        },

        calculate_pts:function(){
          for(var i=0; i<this.players.length;i++){
            this.calculate_player_pts(this.players[i]);
          }
          this.players.sort(compare_players);
        },
        build_players:function(){
          for (var i = 0; i < this.predictions.length; i++) {
                var prediction = this.predictions[i];
                var player = this.find_player(prediction.player);
                if(player == null){
                  player = {name:prediction.player, predictions:[], winner:"", pts:0};
                  this.players.push(player);
                }

                player.predictions.push(prediction);
          }

          for (var i = 0; i < this.winner_predictions.length; i++) {
              var winner = this.winner_predictions[i];
              var player = this.find_player(winner.player);
              if(player == null){
                player = {name:winner.player, predictions:[], winner:"", pts:0};
                this.players.push(player);
              }
              player.winner = winner.winner;
          }

          this.calculate_pts();
        },
        build_prediction:function (player){
                for (var i = 0; i < this.series.length; i++) {
                        var serie = this.series[i]
                        var home = this.get_team_info(serie.home);
                        var visitor = this.get_team_info(serie.visitor);
                        var prediction = this.find_prediction(player, home.id,visitor.id);
                        var win_team = "";
                        var win_games = 4;
                        if(prediction != null){
                                win_team = prediction.win_team;
                                win_games = prediction.win_games;
                        }

                        this.predictions_table[i] = {"round":serie.round, "home":home, "visitor":visitor, "win_team":win_team, "win_games":win_games};
                }
                this.predictions_table.sort(compare_predictions);
        },

        find_winner_prediction:function(player){
                for (var i = 0; i < this.winner_predictions.length; i++) {
                        var prediction = this.winner_predictions[i];
                        if(prediction.player == player){
                                return prediction;
                        }
                }
                return null;
        },

        find_serie:function(home,visitor){
          for (var i = 0; i < this.series.length; i++) {
              var serie = this.series[i];
              if(serie.home == home && serie.visitor==visitor)
                return serie;
          }
          return null;
        },
        find_prediction:function(player, home, visitor){
                for (var i = 0; i < this.predictions.length; i++) {
                        var prediction = this.predictions[i];
                        if(prediction.player == player && prediction.home == home && prediction.visitor == visitor){
                                return prediction;
                        }
                }
                return null;
        },

        get_team_info:function(team_id){
                for (var i = 0; i < this.teams.length; i++) {
                        if(this.teams[i].id == team_id)
                                return this.teams[i];
                }
                return null;
        },

        find_player:function(player){
                for(var i=0; i < this.players.length; i++){
                    if(this.players[i].name == player)
                        return this.players[i];
                }
                return null;
        },

        update:function(){
                this.get_current_round();
                this.get_teams();
                this.get_predictions();
                this.get_series();
                this.get_winner_predictions();
        },

}

        return newobj;
}
