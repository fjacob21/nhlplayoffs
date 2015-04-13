var active_player = "";
var year = "2015";
var teams;
var series;
var predictions=[];
var current_round=0;
var predictions_table;

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

function set_series(round, home, visitor, home_wins, visitor_win) {
        data ={"round":round, "home":home, "visitor":visitor, "home_win":home_wins, "visitor_win":visitor_win};
        //$.postJSON(build_request_url("predictions"), data);
        $.ajax({
            url: build_request_url("series"),
            type: "POST",
            dataType: "json",
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),
            success: function (json) {
                    result = json.prediction;
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

function get_series() {
    $.ajax({
        url: build_request_url("series"),
        type: "GET",
        dataType: "json",
        success: function (json) {
            series = json.series;
            display_series();
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
function apply_series(){
        for (var i = 0; i < series.length; i++) {
                serie = series[i]
                round = $("#" + serie.home+serie.visitor + "_round").val();
                home = $("#" + serie.home+serie.visitor + "_home").val();
                visitor = $("#" + serie.home+serie.visitor + "_visitor").val();
                home_win = $("#" + serie.home+serie.visitor + "_home_win").val();
                visitor_win = $("#" + serie.home+serie.visitor + "_visitor_win").val();

                serie.round = round;
                serie.home = home;
                serie.visitor = visitor;
                serie.home_win = home_win;
                serie.visitor_win = visitor_win;
                set_series(serie.round, serie.home, serie.visitor, serie.home_win, serie.visitor_win);
        }
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

function display_series(){
  for (var i = 0; i < series.length; i++) {
                serie = series[i]

                series_html = "";
                series_html += "<tr class='active'>";
                series_html += "<th>";
                series_html += "<input type='text' id='"+ serie.home+serie.visitor+"_round' value='"+ serie.round +"'>";
                series_html += "</th>";
                series_html += "<th>";
                series_html += "<input type='text' id='"+ serie.home+serie.visitor+"_home' value='"+ serie.home +"'>";
                series_html += "</th>";
                series_html += "<th>";
                series_html += "<input type='text' id='"+ serie.home+serie.visitor+"_visitor' value='"+ serie.visitor +"'>";
                series_html += "</th>";
                series_html += "<th>";
                series_html += "<input type='text' id='"+ serie.home+serie.visitor+"_home_win' value='"+ serie.home_win +"'>";
                series_html += "</th>";
                series_html += "<th>";
                series_html += "<input type='text' id='"+ serie.home+serie.visitor+"_visitor_win' value='"+ serie.visitor_win +"'>";
                series_html += "</th>";
                series_html += "</tr>";
                $("#series_list").append(series_html);
            }
            $("#bt_apply").click(function () {
                    apply_series();
                });
}

function SetSelectedNav(selectednav) {
    if(selectednav == 0){ //Home
        $("#about").hide(500);
        $("#contact").hide(500);
        $("#result").hide(500);
        $("#home").show(500);
    }else if (selectednav == 1) { //About
        $("#home").hide(500);
        $("#contact").hide(500);
        $("#result").hide(500);
        $("#about").show(500);
    }else if (selectednav == 2) { //Contact
        $("#home").hide(500);
        $("#about").hide(500);
        $("#result").hide(500);
        $("#contact").show(500);
}else if (selectednav == 3) { //Results
        $("#home").hide(500);
        $("#about").hide(500);
        $("#contact").hide(500);
        $("#result").show(500);
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

    $('#nav-result').click(function (event) {
        $(this).addClass('active').siblings().removeClass('active');
        SetSelectedNav(3);
    });
}

function Main() {
  RegisterMenuAction();
  get_current_round();
  get_teams();
  get_series();
}
