var active_player = "";
var year = 2015;
var db = new data(year);

function apply_predictions(){
        for (var i = 0; i < db.predictions_table.length; i++) {
                var prediction = db.predictions_table[i]
                var win_team = $("#" + prediction.home.id+prediction.visitor.id + " .active").data('value');
                var win_games = $("#" + prediction.home.id+prediction.visitor.id + "_win_game").val();
                if(win_team != undefined){
                        prediction.win_team = win_team;
                        prediction.win_games = win_games;
                        if(!db.set_prediction(active_player,prediction.home.id, prediction.visitor.id, prediction.win_team, prediction.win_games)){
                                display_error("Cannot submit prediction, try again :(");
                                return false;
                        }
                }
        }
        display_success("All prediction submited with success");
        return true;
}

function apply_winner_predictions(){
        if(!db.set_winner_predictions(active_player,$("#winner_prediction").val()))
            display_error("Cannot submit Stanley cup winner prediction, try again :(");
        else
            display_success("Stanley cup winner prediction submited with success");
        return true;
}

function display_winner_prediction(){
        var series_html = "";
        series_html += "<tr class='active'>";
        series_html += "<th>";

        if(db.round == 1){
          series_html += "<select class='form-control' id='winner_prediction'>";
          for (var i = 0; i < db.teams.length; i++) {
                  var team = db.teams[i]
                  if(team.rank < 9){
                          series_html += "<option value='"+ team.id+"'>"+ team.name +"</option>";
                  }
          }
          series_html += "</th>";
          series_html += "</tr>";
          $("#winner_predictions_list").append(series_html);
          var winner_prediction = db.find_winner_prediction(active_player);
          if(winner_prediction != null)
            $("#winner_prediction").val(winner_prediction.winner)

          $("#bt_winner_apply").click(function () {
            apply_winner_predictions();
          });
        }
        else{
          var winner_prediction = db.find_winner_prediction(active_player);
          if(winner_prediction != null){
            var team = db.get_team_info(winner_prediction.winner);
            series_html += "<img src='http://cdn.nhle.com/nhl/images/logos/teams/"+ team.name.toLowerCase() + "_logo.svgz'>" + team.name;
            series_html += "</th>";
            series_html += "</tr>";
            $("#winner_predictions_list").append(series_html);

          }
          $("#bt_winner_apply").hide();
        }
}

function display_series(){
  for (var i = 0; i < db.predictions_table.length; i++) {
                var prediction = db.predictions_table[i]
                if(prediction.round == db.round){
                        var predict_html = "";
                        predict_html += "<tr class='active'>";
                        predict_html += "<th>";
                        predict_html += "<div class='btn-group' data-toggle='buttons'id='"+ prediction.home.id+prediction.visitor.id+"'>";
                        if(prediction.home.id == prediction.win_team)
                                predict_html += "<label class='btn btn-primary active' style='width:200px' data-value='" + prediction.home.id + "'>";
                        else
                                predict_html += "<label class='btn btn-primary' style='width:200px' data-value='" + prediction.home.id + "'>";
                        predict_html += "<img src='http://cdn.nhle.com/nhl/images/logos/teams/"+ prediction.home.name.toLowerCase() + "_logo.svgz'>";
                        predict_html += "<input type='radio' name='options' id='" + prediction.home.id + "' autocomplete='off'>" + prediction.home.rank + " - " + prediction.home.name;
                        predict_html += "</label>";
                        if(prediction.visitor.id == prediction.win_team)
                                predict_html += "<label class='btn btn-primary active' style='width:200px' data-value='" + prediction.visitor.id + "'>";
                        else
                                predict_html += "<label class='btn btn-primary' style='width:200px' data-value='" + prediction.visitor.id + "'>";
                        predict_html += "<img src='http://cdn.nhle.com/nhl/images/logos/teams/"+ prediction.visitor.name.toLowerCase() + "_logo.svgz'>";
                        predict_html += "<input type='radio' name='options' id='" + prediction.visitor.id + "' autocomplete='off'>" + prediction.visitor.rank + " - " + prediction.visitor.name;
                        predict_html += "</label>";
                        predict_html += "</div>";
                        predict_html += "</th>";
                        predict_html += "<th>";
                        predict_html += "<select class='form-control' id='"+ prediction.home.id+prediction.visitor.id+"_win_game'>";
                        predict_html += "<option>4</option>";
                        predict_html += "<option>5</option>";
                        predict_html += "<option>6</option>";
                        predict_html += "<option>7</option>";
                        predict_html += "</select>";
                        predict_html += "</th>";
                        predict_html += "</tr>";
                        $("#predictions_list").append(predict_html);
                        $("#"+ prediction.home.id+prediction.visitor.id+"_win_game").val(prediction.win_games);
                }
            }
            $("#bt_apply").click(function () {
                    apply_predictions();
                });
}

function find_player_serie (predictions,home,visitor){
  for (var i = 0; i < predictions.length; i++) {
      var serie = predictions[i];
      if(serie.home == home && serie.visitor==visitor)
        return serie;
  }
  return null;
}

function team_img(team){
  return "http://cdn.nhle.com/nhl/images/logos/teams/"+ team.name.toLowerCase() + "_logo.svgz";
}

var round_color = ['#B0B0B0', '#A0A0A0', '#909090', '#808080', '#707070'];
function display_reviews(){
        $("#review_series").empty();
        $("#review_series").append("<th>Player</th>");
        for(var i=0;i<db.series.length;i++){
                var serie = db.series[i];
                var home = db.get_team_info(serie.home);
                var visitor = db.get_team_info(serie.visitor);
                var series_html = "";
                series_html += "<th style='background-color: #404040'>";
                series_html += "<img  height='20' width='20' title='"+ home.name + "' src='"+ team_img(home) + "'>";
                series_html += "<img  height='20' width='20' title='"+ visitor.name + "' src='"+ team_img(visitor) + "'>";
                series_html += "</th>";
                $("#review_series").append(series_html);
        }
        $("#review_series").append("<th width='20'>Pts</th>");

        $("#review_list").empty();
        for (var i = 0; i < db.players.length; i++) {
                      var player = db.players[i]
                      var series_html = "";
                      series_html += "<tr class='active'>";
                      series_html += "<th style='vertical-align: middle'>";
                      series_html += player.name;
                      series_html += "</th>";
                      for(var j=0;j<db.series.length;j++){
                             var serie = db.series[j];
                             var prediction = find_player_serie(player.predictions,serie.home,serie.visitor);

                             series_html += "<th style='vertical-align: middle;background-color: " + round_color[serie.round-1] + "'>";
                             if(prediction!=null && serie.round < db.round){
                                var team = db.get_team_info(prediction.win_team);
                                series_html += prediction.win_games;
                                series_html += "<img  height='42' width='42' title='"+ team.name + "' src='"+ team_img(team) + "'>";
                             }
                             else
                                series_html += "?";
                             series_html += "</th>";
                      }
                      series_html += "<th style='vertical-align: middle'>";
                      series_html += player.pts;
                      series_html += "</th>";
                      series_html += "</tr>";
                      $("#review_list").append(series_html);
                  }
}

function display_error(msg){
        $("#error-alert").html(msg);
        $("#error-alert").show();
        $("#error-alert").fadeTo(2000, 500).slideUp(500);
}

function display_success(msg){
        $("#success-alert").html(msg);
        $("#success-alert").show();
        $("#success-alert").fadeTo(2000, 500).slideUp(500);
}

function login_submit(){
        active_player = $("#login_player").val();
        if(active_player != "") {
          $('#login_modal').modal('hide')
          db.onDataLoaded = function(){
            db.build_players();
            db.build_prediction(active_player);
            display_series();
            display_winner_prediction();
            display_reviews();};
          db.update();
        }
}

function login(){
  $("#btlogin").click(function () {
          login_submit()
  });
  $('#login_modal').on('shown.bs.modal', function () {
    $('#login_player').focus();
})
$('#login_form').submit(function(event){

  // prevent default browser behaviour
  event.preventDefault();
  login_submit()
});

  $('#login_modal').modal({
                            backdrop: 'static',
                            keyboard: false
                          })
        $('#login_player').focus();
}

function SetSelectedNav(selectednav) {
    if(selectednav == 0){ //Home
        $("#about").hide(500);
        $("#contact").hide(500);
        $("#review").hide(500);
        $("#home").show(500);
    }else if (selectednav == 1) { //About
        $("#home").hide(500);
        $("#contact").hide(500);
        $("#review").hide(500);
        $("#about").show(500);
    }else if (selectednav == 2) { //Contact
        $("#home").hide(500);
        $("#about").hide(500);
        $("#review").hide(500);
        $("#contact").show(500);
    }else if (selectednav == 3) { //Review
        $("#home").hide(500);
        $("#about").hide(500);
        $("#contact").hide(500);
        $("#review").show(500);
    }
}

function RegisterMenuAction() {
    $('#nav-home').click(function (event) {
        $(this).addClass('active').siblings().removeClass('active');
        SetSelectedNav(0);
    });

    $('#nav-about').click(function (event) {
        $(this).addClass('active').siblings().removeClass('active');
        SetSelectedNav(1);
    });

    $('#nav-contact').click(function (event) {
        $(this).addClass('active').siblings().removeClass('active');
        SetSelectedNav(2);
    });

    $('#nav-review').click(function (event) {
        $(this).addClass('active').siblings().removeClass('active');
        SetSelectedNav(3);
    });
}

function Main() {
  RegisterMenuAction();

  login();
}
