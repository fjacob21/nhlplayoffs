import requests

class NHLQuery(object):

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

    def get_teams(self):
        ystr = str(self._year) + str(self._year + 1)
        url = 'https://statsapi.web.nhl.com/api/v1/standings?season=' + ystr
        standings = requests.get(url).json()
        teams = {}
        for record in standings["records"]:
            for team in record['teamRecords']:
                info = self.get_team(team['team']['id'])
                team_record = {'info': info, 'standings': team, 'schedule': []}
                teams[team['team']['id']] = team_record
        return teams
    
    def get_schedule(self, team):
        # print('Get schedule for ' + str(team))
        url = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate=' + str(self._year) + '-10-01&endDate=' + str(self._year + 1) + '-05-29&expand=schedule.teams,schedule.linescore,schedule.broadcasts,schedule.ticket,schedule.game.content.media.epg&leaderCategories=&site=en_nhlCA&teamId=' + str(team)
        team_schedule = requests.get(url)
        return team_schedule.json()

    def get_playoff_schedule(self, team):
        url = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate=' + str(self._year + 1) + '-04-01&endDate=' + str(self._year + 1) + '-10-15&expand=schedule.teams,schedule.linescore,&site=en_nhlCA&teamId=' + str(team)
        # print(url)
        team_schedule = requests.get(url)
        return team_schedule.json()