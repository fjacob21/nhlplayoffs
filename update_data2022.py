#!/usr/bin/env python3
import argparse
from updater import Updater

class Updater2022(Updater):

    def __init__(self, server):
        super(Updater2022, self).__init__(server, 2021)
        self._auto_move = True
    
    def run(self):
        if self._current_round == 0:
            self._teams = self._query.get_teams()
            self.create_matchups_tree()

            if len(self.teams) > 0:
                self._standings = self.get_season_standings()
                self.create_matchups(self._standings, 0)
                if self.is_season_finished():
                    self._current_round += 1
            self.store()
        else:
            self.update_matchups()
            # if self.is_round_finished(self._current_round):
            #     self.create_matchups(self.get_round_winners_standings(self._current_round), self._current_round)
            #     self._current_round += 1
            # self.store()
    
    def create_matchups_tree(self):
        sc = self._matchups.create_matchup('sc', 4, None)
        self._matchups[sc['id']] = sc

        sc1 = self._matchups.create_matchup('sc1', 3, sc)
        sc2 = self._matchups.create_matchup('sc2', 3, sc)
        self._matchups[sc1['id']] = sc1
        self._matchups[sc2['id']] = sc2

        a = self._matchups.create_matchup('a', 2, sc2)
        m = self._matchups.create_matchup('m', 2, sc2)
        c = self._matchups.create_matchup('c', 2, sc1)
        p = self._matchups.create_matchup('p', 2, sc1)
        self._matchups[a['id']] = a
        self._matchups[m['id']] = m
        self._matchups[c['id']] = c
        self._matchups[p['id']] = p

        a1 = self._matchups.create_matchup('a1', 1, a)
        a2 = self._matchups.create_matchup('a2', 1, a)
        m1 = self._matchups.create_matchup('m1', 1, m)
        m2 = self._matchups.create_matchup('m2', 1, m)
        c1 = self._matchups.create_matchup('c1', 1, c)
        c2 = self._matchups.create_matchup('c2', 1, c)
        p1 = self._matchups.create_matchup('p1', 1, p)
        p2 = self._matchups.create_matchup('p2', 1, p)
        self._matchups[a1['id']] = a1
        self._matchups[a2['id']] = a2
        self._matchups[m1['id']] = m1
        self._matchups[m2['id']] = m2
        self._matchups[c1['id']] = c1
        self._matchups[c2['id']] = c2
        self._matchups[p1['id']] = p1
        self._matchups[p2['id']] = p2

        # build tree
        self._matchups.set_matchup_childs(sc, sc1, sc2)

        self._matchups.set_matchup_childs(sc2, a, m)
        self._matchups.set_matchup_childs(sc1, c, p)

        self._matchups.set_matchup_childs(a, a2, a1)
        self._matchups.set_matchup_childs(m, m2, m1)
        self._matchups.set_matchup_childs(c, c2, c1)
        self._matchups.set_matchup_childs(p, p2, p1)
    
    def get_standings(self, teams):
        standings = {'Eastern': {'Atlantic': [], 'Metropolitan': [], 'teams': []}, 'Western': {'Central': [], 'Pacific': [], 'teams': []}, 'teams': []}

        league = sorted(list(self._teams.values()), key=lambda k: int(k['standings']['divisionRank']))
        for team in league:
            standings['teams'].append(team)
            standings[team['info']['conference']['name']]['teams'].append(team)
            standings[team['info']['conference']['name']][team['info']['division']['name']].append(team)
        standings['teams'] = sorted(standings['teams'], key=lambda k: int(k['standings']['leagueRank']))

        standings['Eastern']['teams'] = sorted(standings['Eastern']['teams'], key=lambda k: int(k['standings']['conferenceRank']))
        standings['Western']['teams'] = sorted(standings['Western']['teams'], key=lambda k: int(k['standings']['conferenceRank']))

        standings['Eastern']['Atlantic'] = sorted(standings['Eastern']['Atlantic'], key=lambda k: int(k['standings']['divisionRank']))
        standings['Eastern']['Metropolitan'] = sorted(standings['Eastern']['Metropolitan'], key=lambda k: int(k['standings']['divisionRank']))
        standings['Western']['Central'] = sorted(standings['Western']['Central'], key=lambda k: int(k['standings']['divisionRank']))
        standings['Western']['Pacific'] = sorted(standings['Western']['Pacific'], key=lambda k: int(k['standings']['divisionRank']))
        return standings
    
    def create_matchups_round0(self, standings):
        ealeader = standings['Eastern']['Atlantic'][0]
        emleader = standings['Eastern']['Metropolitan'][0]
        wcleader = standings['Western']['Central'][0]
        wpleader = standings['Western']['Pacific'][0]
        for team in standings['Eastern']['teams']:
            if int(team['standings']['wildCardRank']) == 1:
                e1wild = team
            if int(team['standings']['wildCardRank']) == 2:
                e2wild = team

        for team in standings['Western']['teams']:
            if int(team['standings']['wildCardRank']) == 1:
                w1wild = team
            if int(team['standings']['wildCardRank']) == 2:
                w2wild = team

        if int(ealeader['standings']['conferenceRank']) < int(emleader['standings']['conferenceRank']):
            a1_teams = (ealeader, e2wild)
            m1_teams = (emleader, e1wild)
        else:
            a1_teams = (ealeader, e1wild)
            m1_teams = (emleader, e2wild)
        a2_teams = (standings['Eastern']['Atlantic'][1], standings['Eastern']['Atlantic'][2])
        m2_teams = (standings['Eastern']['Metropolitan'][1], standings['Eastern']['Metropolitan'][2])

        if int(wcleader['standings']['conferenceRank']) < int(wpleader['standings']['conferenceRank']):
            c1_teams = (wcleader, w2wild)
            p1_teams = (wpleader, w1wild)
        else:
            c1_teams = (wcleader, w1wild)
            p1_teams = (wpleader, w2wild)
        c2_teams = (standings['Western']['Central'][1], standings['Western']['Central'][2])
        p2_teams = (standings['Western']['Pacific'][1], standings['Western']['Pacific'][2])

        a1 = self._matchups['a1']
        a2 = self._matchups['a2']
        m1 = self._matchups['m1']
        m2 = self._matchups['m2']
        self.update_matchup(a1, a1_teams[0]['info']['id'], a1_teams[1]['info']['id'])
        self.update_matchup(a2, a2_teams[0]['info']['id'], a2_teams[1]['info']['id'])
        self.update_matchup(m1, m1_teams[0]['info']['id'], m1_teams[1]['info']['id'])
        self.update_matchup(m2, m2_teams[0]['info']['id'], m2_teams[1]['info']['id'])
        c1 = self._matchups['c1']
        c2 = self._matchups['c2']
        p1 = self._matchups['p1']
        p2 = self._matchups['p2']
        self.update_matchup(c1, c1_teams[0]['info']['id'], c1_teams[1]['info']['id'])
        self.update_matchup(c2, c2_teams[0]['info']['id'], c2_teams[1]['info']['id'])
        self.update_matchup(p1, p1_teams[0]['info']['id'], p1_teams[1]['info']['id'])
        self.update_matchup(p2, p2_teams[0]['info']['id'], p2_teams[1]['info']['id'])
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update the nhlpool database')
    parser.add_argument('-s', '--server', metavar='server', default='debug', nargs='?',
                        help='The server to use')

    args = parser.parse_args()

    if args.server == 'prod':
        print('Using production server')
        server = 'nhlpool.robalab.net/'
    else:
        print('Using debug server')
        server = 'localhost:5000'

    upd = Updater2022(server)
    upd.run()
    upd.display()
