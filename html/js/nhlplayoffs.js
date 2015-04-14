var active_player = "";
var year = "2015";
var teams;
var series;
var predictions=[];
var current_round=0;
var predictions_table;
var winner_predictions;

function build_request_url(request){
        return "/nhlplayoffs/api/v1.0/" + year + "/"+request;
}

function get_request(request, result){
        $.ajax({
            url: build_request_url(request),
            type: "GET",
            dataType: "json",
            success: function (json) {
                result = json;
            },
            error: function (xhr, status, errorThrown) {
                //alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
                console.dir(xhr);
            },
            complete: function (xhr, status) {
                //alert("The request is complete!");
            }
        });
}

function get_predictions() {
        $.ajax({
            url: build_request_url("predictions"),
            type: "GET",
            dataType: "json",
            success: function (json) {
                    predictions_table = json.predictions;
            },
            error: function (xhr, status, errorThrown) {
                //alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
                console.dir(xhr);
            },
            complete: function (xhr, status) {
                //alert("The request is complete!");
            }
        });
}

function set_predictions(home, visitor, win_team, win_games) {
        data ={"player":active_player, "home":home, "visitor":visitor, "win_team":win_team, "win_games":win_games};
        //$.postJSON(build_request_url("predictions"), data);
        var result = $.ajax({
            url: build_request_url("predictions"),
            type: "POST",
            dataType: "json",
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),
            async: false
        });
        if(result.status != 201 )
                return false;
        return true;
}

function get_winner_predictions() {
        $.ajax({
            url: build_request_url("winner_predictions"),
            type: "GET",
            dataType: "json",
            success: function (json) {
              winner_predictions = json.winner_predictions;
            },
            error: function (xhr, status, errorThrown) {
                //alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
                console.dir(xhr);
            },
            complete: function (xhr, status) {
                //alert("The request is complete!");
            }
        });
}

function set_winner_predictions(winner) {
        data ={"player":active_player, "winner":winner};
        //$.postJSON(build_request_url("predictions"), data);
        var result = $.ajax({
            url: build_request_url("winner_predictions"),
            type: "POST",
            dataType: "json",
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),
            async: false
        });
        if(result.status != 201 )
                return false;
        return true;
}

function get_teams() {
        $.ajax({
            url: build_request_url("teams"),
            type: "GET",
            dataType: "json",
            success: function (json) {
                teams = json.teams;
            },
            error: function (xhr, status, errorThrown) {
                //alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
                console.dir(xhr);
            },
            complete: function (xhr, status) {
                //alert("The request is complete!");
            }
        });
}

function get_current_round() {
    $.ajax({
        url: build_request_url("current_round"),
        type: "GET",
        dataType: "json",
        success: function (json) {
          current_round = json.current_round;
        },
        error: function (xhr, status, errorThrown) {
            //alert("Sorry, there was a problem!");
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        },
        complete: function (xhr, status) {
            //alert("The request is complete!");
        }
    });
}

function compare_predictions(a,b) {
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

function build_prediction(){
  for (var i = 0; i < series.length; i++) {
                serie = series[i]
                home = get_team_info(serie.home);
                visitor = get_team_info(serie.visitor);
                prediction = find_prediction(home.id,visitor.id);
                var win_team = "";
                var win_games = 4;
                if(prediction != null){
                        win_team = prediction.win_team;
                        win_games = prediction.win_games;
                }
                predictions[i] = {"round":serie.round, "home":home, "visitor":visitor, "win_team":win_team, "win_games":win_games};
                }
                predictions.sort(compare_predictions);
}

function get_series() {
    $.ajax({
        url: build_request_url("series"),
        type: "GET",
        dataType: "json",
        success: function (json) {
            series = json.series;
        },
        error: function (xhr, status, errorThrown) {
            //alert("Sorry, there was a problem!");
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        },
        complete: function (xhr, status) {
            //alert("The request is complete!");
        }
    });
}
function apply_predictions(){
        for (var i = 0; i < predictions.length; i++) {
                prediction = predictions[i]
                win_team = $("#" + prediction.home.id+prediction.visitor.id + " .active").data('value');
                win_games = $("#" + prediction.home.id+prediction.visitor.id + "_win_game").val();
                prediction.win_team = win_team;
                prediction.win_games = win_games;
                if(!set_predictions(prediction.home.id, prediction.visitor.id, prediction.win_team, prediction.win_games)){
                        display_error("Cannot submit prediction, try again :(");
                        return false;
                }
        }
        display_success("All prediction submited with success");
        return true;
}

function apply_winner_predictions(){
        if(!set_winner_predictions($("#winner_prediction").val()))
            display_error("Cannot submit Stanley cup winner prediction, try again :(");
        else
            display_success("Stanley cup winner prediction submited with success");
        return true;
}

function find_winner_prediction(){
  for (var i = 0; i < winner_predictions.length; i++) {
          prediction = winner_predictions[i];
          if(prediction.player == active_player){
                  return prediction;
          }
  }
  return null;
}

function find_prediction(home, visitor){
        for (var i = 0; i < predictions_table.length; i++) {
                prediction = predictions_table[i];
                if(prediction.player == active_player && prediction.home == home && prediction.visitor == visitor){
                        return prediction;
                }
        }
        return null;
}

function get_team_info(team_id){
  for (var i = 0; i < teams.length; i++) {
      if(teams[i].id == team_id)
        return teams[i];
  }
  return null;
}

function display_winner_prediction(){
        series_html = "";
        series_html += "<tr class='active'>";
        series_html += "<th>";

        if(current_round == 1){
          series_html += "<select class='form-control' id='winner_prediction'>";
          for (var i = 0; i < teams.length; i++) {
                  team = teams[i]
                  if(team.rank < 9){
                          series_html += "<option value='"+ team.id+"'>"+ team.name +"</option>";
                  }
          }
          series_html += "</th>";
          series_html += "</tr>";
          $("#winner_predictions_list").append(series_html);
          winner_prediction = find_winner_prediction();
          if(winner_prediction != null)
            $("#winner_prediction").val(winner_prediction.winner)

          $("#bt_winner_apply").click(function () {
            apply_winner_predictions();
          });
        }
        else{
          winner_prediction = find_winner_prediction();
          if(winner_prediction != null){
            team = get_team_info(winner_prediction.winner);
            series_html += "<img src='http://cdn.nhle.com/nhl/images/logos/teams/"+ team.name.toLowerCase() + "_logo.svgz'>" + team.name;
            series_html += "</th>";
            series_html += "</tr>";
            $("#winner_predictions_list").append(series_html);
            $("#bt_winner_apply").hide();
          }
        }
}

function display_series(){
  for (var i = 0; i < predictions.length; i++) {
                prediction = predictions[i]
                if(prediction.round == current_round){
                        predict_html = "";
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
          build_prediction();
          display_series();
          display_winner_prediction();
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
  get_current_round();
  get_predictions();
  get_winner_predictions();
  get_teams();
  get_series();

  login();


}
