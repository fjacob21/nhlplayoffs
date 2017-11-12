import requests


class NHLData(object):

    def __init__(self, year):
        self._year = year
        self._teams = None
        self._standings = None

    def get_team(self, id):
        url = 'https://statsapi.web.nhl.com/api/v1/teams/' + str(id)
        team = requests.get(url).json()
        return team['teams'][0]

    def get_standings(self):
        if not self._standings:
            ystr = str(self._year) + str(self._year + 1)
            url = 'https://statsapi.web.nhl.com/api/v1/standings?season=' + ystr
            standings = requests.get(url).json()
            self._standings = standings["records"]
        return self._standings

    def get_schedule(self, team):
        print('Get schedule for ' + str(team))
        url = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate=' + str(self._year) + '-10-01&endDate=' + str(self._year + 1) + '-06-29&expand=schedule.teams,schedule.linescore,schedule.broadcasts,schedule.ticket,schedule.game.content.media.epg&leaderCategories=&site=en_nhlCA&teamId=' + str(team)
        team_schedule = requests.get(url)
        return team_schedule.json()

    def get_playoff_schedule(self, team):
        url = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate=' + str(self._year + 1) + '-04-01&endDate=' + str(self._year + 1) + '-06-29&expand=schedule.teams,&site=en_nhlCA&teamId=' + str(team)
        team_schedule = requests.get(url)
        return team_schedule.json()

    def get_teams(self):
        if not self._teams:
            standings = self.get_standings()
            teams = {}
            for record in standings:
                for team in record['teamRecords']:
                    info = self.get_team(team['team']['id'])
                    team_record = {'info': info, 'standings': team, 'schedule': []}
                    teams[team['team']['id']] = team_record
            self._teams = teams
        return self._teams
