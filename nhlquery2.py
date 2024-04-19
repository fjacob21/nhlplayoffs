import requests

class NHLQuery2(object):

    def __init__(self, year):
        self._year = year
    
    def get_live_result(self, link):
        url = 'https://statsapi.web.nhl.com' + link
        live = requests.get(url).json()
        return live

    def get_team(self, id):
        url = 'https://statsapi.web.nhl.com/api/v1/teams/' + str(id)
        team = requests.get(url).json()
        return team['teams'][0]

    def _get_team_ids(self):
        url = 'https://api.nhle.com/stats/rest/en/franchise?sort=fullName&include=lastSeason.id&include=firstSeason.id'
        team_res = requests.get(url).json()
        teams = team_res["data"]
        team_ids = {}
        for team in teams:
            team_ids[team["fullName"]] = team["id"]
        return team_ids
    
    def get_teams(self):
        team_ids = self._get_team_ids()
        url = "https://api-web.nhle.com/v1/standings/now"
        standings = requests.get(url).json()
        teams = {}
        for team in standings["standings"]:
            # team_id = team_ids[team['teamName']['default']]
            team_id = team['teamAbbrev']['default']
            leagueRecord_obj = {"losses": team["losses"], "wins": team["wins"], "ot": team["otLosses"]}
            standings_obj = {
                "conferenceRank": team["conferenceSequence"],
                "divisionRank": team["divisionSequence"],
                "leagueRank": team["leagueSequence"],
                "wildCardRank": team["wildcardSequence"],
                "gamesPlayed": team["gamesPlayed"],
                "points": team["points"],
                "leagueRecord": leagueRecord_obj
            }
            conference_obj = {"name": team["conferenceName"]}
            division_obj = {"name": team["divisionName"]}
            info_obj = {"name": team["teamName"]["default"], "id": team_id, "abbreviation": team['teamAbbrev']['default'], "conference": conference_obj, "division": division_obj}
            team_record = {'info': info_obj, 'standings': standings_obj, 'schedule': []}
            teams[team_id] = team_record
        return teams
    
    def get_schedule(self, team):
        print('Get schedule for ' + str(team))
        url = 'https://api-web.nhle.com/v1/club-schedule-season/' + str(team) + '/' + str(self._year) + str(self._year + 1)
        team_schedule = requests.get(url).json()
        dates = []
        for game_data in team_schedule["games"]:
            if game_data["gameType"] == 2:
                home_score = 0
                away_score = 0
                if game_data["gameState"] == "OFF":
                    home_score = game_data["homeTeam"]["score"]
                    away_score = game_data["awayTeam"]["score"]
                home_team = {"id": game_data["homeTeam"]["abbrev"]}
                home_team_game = {"team": home_team, "score": home_score}
                away_team = {"id": game_data["awayTeam"]["abbrev"]}
                away_team_game = {"team": away_team, "score": away_score}
                game = {"teams": {"home": home_team_game, "away": away_team_game}, "gameType": "R", "gameDate": game_data["startTimeUTC"]}
                dates.append({"games": [game]})
        schedules = {"dates": dates}
        return schedules

    def get_playoff_schedule(self, team):
        # url = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate=' + str(self._year + 1) + '-04-01&endDate=' + str(self._year + 1) + '-10-15&expand=schedule.teams,schedule.linescore,&site=en_nhlCA&teamId=' + str(team)
        # # print(url)
        # team_schedule = requests.get(url)
        # return team_schedule.json()
        url = 'https://api-web.nhle.com/v1/club-schedule-season/' + str(team) + '/' + str(self._year) + str(self._year + 1)
        team_schedule = requests.get(url).json()
        dates = []
        for game_data in team_schedule["games"]:
            if game_data["gameType"] == 3:
                home_score = 0
                away_score = 0
                status = 1
                if game_data["gameState"] == "OFF":
                    home_score = game_data["homeTeam"]["score"]
                    away_score = game_data["awayTeam"]["score"]
                    status = 7
                home_team = {"id": game_data["homeTeam"]["abbrev"]}
                home_team_game = {"team": home_team, "score": home_score}
                away_team = {"id": game_data["awayTeam"]["abbrev"]}
                away_team_game = {"team": away_team, "score": away_score}
                game_status = {"statusCode": status}
                game = {"teams": {"home": home_team_game, "away": away_team_game}, "gameType": "P", "gameDate": game_data["startTimeUTC"], "status": game_status}
                dates.append({"games": [game]})
        schedules = {"dates": dates}
        return schedules