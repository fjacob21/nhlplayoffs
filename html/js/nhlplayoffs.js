var active_player = "";
var year = 2015;
var db = new data(year);

function apply_predictions(){
        for (var i = 0; i < db.predictions_table.length; i++) {
                var prediction = db.predictions_table[i]
                var win_team = $("#" + prediction.home.id+prediction.visitor.id + " .active").data('value');
                var win_games = $("#" + prediction.home.id+prediction.visitor.id + "_win_game").val();
                prediction.win_team = win_team;
                prediction.win_games = win_games;
                if(!db.set_prediction(active_player,prediction.home.id, prediction.visitor.id, prediction.win_team, prediction.win_games)){
                        display_error("Cannot submit prediction, try again :(");
                        return false;
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
          var winner_prediction = find_winner_prediction();
          if(winner_prediction != null){
            var team = get_team_info(winner_prediction.winner);
            series_html += "<img src='http://cdn.nhle.com/nhl/images/logos/teams/"+ team.name.toLowerCase() + "_logo.svgz'>" + team.name;
            series_html += "</th>";
            series_html += "</tr>";
            $("#winner_predictions_list").append(series_html);
            $("#bt_winner_apply").hide();
          }
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
            display_winner_prediction();};
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
        $("#home").show(500);
    }else if (selectednav == 1) { //About
        $("#home").hide(500);
        $("#contact").hide(500);
        $("#about").show(500);
    }else if (selectednav == 2) { //Contact
        $("#home").hide(500);
        $("#about").hide(500);
        $("#contact").show(500);
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
}

function Main() {
  RegisterMenuAction();

  login();


}
