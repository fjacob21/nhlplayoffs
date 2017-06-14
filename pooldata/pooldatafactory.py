from datetime import datetime
from dateutil import tz
from game import Game, GAME_STATE_SCHEDULED
from matchup import Matchup
from matchupresult import MatchupResult
from matchupseasonresults import MatchupSeasonResults
from standing import Standing
from team import Team
from teamvenue import TeamVenue


def create_team(id, abbreviation, name, fullname, city, active=False, creation_year=0, website='', venue=None, league_info=None):
    return Team(id, abbreviation, name, fullname, city, active, creation_year, website, venue, league_info)


def create_team_venue(city, name='', timezone='', address=''):
    return TeamVenue(city, name, timezone, address)


def create_standing(team_id, pts, win, losses, ot, games_played, goals_against, goals_scored, ranks, extra_info={}):
    return Standing(team_id, pts, win, losses, ot, games_played, goals_against, goals_scored, ranks, extra_info)


def create_matchup_results(home_win=0, away_win=0):
    return MatchupResult(home_win, away_win)


def create_matchup_season_results(home_win, away_win, games=[]):
    return MatchupSeasonResults(home_win, away_win, games)


def create_matchup_game(home, away, date='', state=GAME_STATE_SCHEDULED, home_goal=0, away_goal=0, extra_data=None):
    return Game(home, away, date, state, home_goal, away_goal, extra_data)


def create_matchup(id, round, home=0, away=0, start='', schedule={}, season_results={}, results=None):
    if not results:
        results = results = create_matchup_results()
    return Matchup(id, round, home, away, start, schedule, season_results, results)


def string_to_date(date):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    utc = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    utc = utc.replace(tzinfo=from_zone)
    return utc.astimezone(to_zone)


def date_to_string(date):
    to_zone = tz.gettz('UTC')
    return date.astimezone(to_zone).strftime('%Y-%m-%dT%H:%M:%SZ')


def now():
    to_zone = tz.gettz('America/New_York')
    return datetime.now(tz.tzlocal()).astimezone(to_zone)


def date(year, month, day, hour=0, minute=0, second=0, tzinfo=tz.gettz('America/New_York')):
    return datetime(year, month, day, hour, minute, second, tzinfo=tzinfo)
