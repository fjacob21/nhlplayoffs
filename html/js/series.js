var active_player = "";
var year = "2015";
var year = 2015;
var db = new data(year);

function apply_series(){
        for (var i = 0; i < db.series.length; i++) {
                var serie = db.series[i]
                var round = $("#" + serie.home+serie.visitor + "_round").val();
                var home = $("#" + serie.home+serie.visitor + "_home").val();
                var visitor = $("#" + serie.home+serie.visitor + "_visitor").val();
                var home_win = $("#" + serie.home+serie.visitor + "_home_win").val();
                var visitor_win = $("#" + serie.home+serie.visitor + "_visitor_win").val();

                serie.round = round;
                serie.home = home;
                serie.visitor = visitor;
                serie.home_win = home_win;
                serie.visitor_win = visitor_win;
                db.set_series(serie.round, serie.home, serie.visitor, serie.home_win, serie.visitor_win);
        }
        db.calculate_pts();
        display_results();
        display_success("All series submited with success");
        return true;
}

function display_series(){
  $("#series_list").empty();
  for (var i = 0; i < db.series.length; i++) {
                var serie = db.series[i]

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

function display_results(){
  $("#results_list").empty();
  for (var i = 0; i < db.players.length; i++) {
                var player = db.players[i]
                var team = db.get_team_info(player.winner);
                series_html = "";
                series_html += "<tr class='active'>";
                series_html += "<th>";
                series_html += player.name;
                series_html += "</th>";
                series_html += "<th>";
                series_html += "<img src='http://cdn.nhle.com/nhl/images/logos/teams/"+ team.name.toLowerCase() + "_logo.svgz'>";
                series_html += "</th>";
                series_html += "<th>";
                series_html += player.pts;
                series_html += "</th>";
                series_html += "</tr>";
                $("#results_list").append(series_html);
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
  db.onDataLoaded = function(){
    db.build_players();
    display_series();
    display_results();};
  db.update();
}
