#!/usr/bin/env python3
import argparse
from updater import Updater

class Updater2021(Updater):

    def __init__(self, server):
        super(Updater2021, self).__init__(server, 2020)
        self._season_games = 56
    
    def run(self):
        print(f"Updater 2021 round:{self._current_round}")
        if self._current_round == 0:
            self._teams = self._query.get_teams()
            self.create_matchups_tree()

            if len(self.teams) > 0:
                self._standings = self.get_season_standings()
                self.create_matchups(self._standings, 0)
                if self.is_season_finished() or self.is_all_matchup_have_start(1):
                    print("Playoffs ready to begin!!!!!")
                    self._current_round += 1
            self.store()
        else:
            self.update_matchups()
            if self.is_round_finished(self._current_round):
                print(f"Round {self._current_round} finished!!!")
                self._current_round += 1
            round1_standing = self.get_round_winners_standings(1)
            round2_standing = self.get_round_winners_standings(2)
            round3_standing = self.get_round_winners_standings(3)
            self.create_matchups(round1_standing, 1)
            self.create_matchups(round2_standing, 2)
            self.create_matchups(round3_standing, 3)
            # self.create_matchups(self.get_round_winners_standings(self._current_round), self._current_round)
            self.store()
    
    def create_matchups_tree(self):
        sc = self._matchups.create_matchup('sc', 4, None)
        self._matchups[sc['id']] = sc

        sc1 = self._matchups.create_matchup('sc1', 3, sc)
        sc2 = self._matchups.create_matchup('sc2', 3, sc)
        self._matchups[sc1['id']] = sc1
        self._matchups[sc2['id']] = sc2

        n = self._matchups.create_matchup('n', 2, sc1)
        c = self._matchups.create_matchup('c', 2, sc1)
        e = self._matchups.create_matchup('e', 2, sc2)
        w = self._matchups.create_matchup('w', 2, sc2)
        self._matchups[n['id']] = n
        self._matchups[c['id']] = c
        self._matchups[e['id']] = e
        self._matchups[w['id']] = w

        n1 = self._matchups.create_matchup('n1', 1, n)
        n2 = self._matchups.create_matchup('n2', 1, n)
        c1 = self._matchups.create_matchup('c1', 1, c)
        c2 = self._matchups.create_matchup('c2', 1, c)
        e1 = self._matchups.create_matchup('e1', 1, e)
        e2 = self._matchups.create_matchup('e2', 1, e)
        w1 = self._matchups.create_matchup('w1', 1, w)
        w2 = self._matchups.create_matchup('w2', 1, w)
        self._matchups[n1['id']] = n1
        self._matchups[n2['id']] = n2
        self._matchups[c1['id']] = c1
        self._matchups[c2['id']] = c2
        self._matchups[e1['id']] = e1
        self._matchups[e2['id']] = e2
        self._matchups[w1['id']] = w1
        self._matchups[w2['id']] = w2

        # build tree
        self._matchups.set_matchup_childs(sc, sc1, sc2)

        self._matchups.set_matchup_childs(sc1, n, c)
        self._matchups.set_matchup_childs(sc2, e, w)

        self._matchups.set_matchup_childs(n, n2, n1)
        self._matchups.set_matchup_childs(c, c2, c1)
        self._matchups.set_matchup_childs(e, e2, e1)
        self._matchups.set_matchup_childs(w, w2, w1)
    
    def get_standings(self, teams):
        standings = {'Scotia North': [], 'Discover Central': [], 'MassMutual East': [], 'Honda West': [], 'teams': []}

        league = sorted(teams, key=lambda k: int(k['standings']['leagueRank']))
        for team in league:
            standings['teams'].append(team)
            standings[team['info']['division']['name']].append(team)
        standings['teams'] = sorted(standings['teams'], key=lambda k: int(k['standings']['leagueRank']))

        standings['Scotia North'] = sorted(standings['Scotia North'], key=lambda k: int(k['standings']['divisionRank']))
        standings['Discover Central'] = sorted(standings['Discover Central'], key=lambda k: int(k['standings']['divisionRank']))
        standings['MassMutual East'] = sorted(standings['MassMutual East'], key=lambda k: int(k['standings']['divisionRank']))
        standings['Honda West'] = sorted(standings['Honda West'], key=lambda k: int(k['standings']['divisionRank']))
        return standings
    
    def create_matchups_round0(self, standings):
        n1 = self._matchups['n1']
        n2 = self._matchups['n2']
        c1 = self._matchups['c1']
        c2 = self._matchups['c2']
        self.update_matchup(n1, standings['Scotia North'][0]['info']['id'], standings['Scotia North'][3]['info']['id'])
        self.update_matchup(n2, standings['Scotia North'][1]['info']['id'], standings['Scotia North'][2]['info']['id'])
        self.update_matchup(c1, standings['Discover Central'][0]['info']['id'], standings['Discover Central'][3]['info']['id'])
        self.update_matchup(c2, standings['Discover Central'][1]['info']['id'], standings['Discover Central'][2]['info']['id'])
        e1 = self._matchups['e1']
        e2 = self._matchups['e2']
        w1 = self._matchups['w1']
        w2 = self._matchups['w2']
        self.update_matchup(e1, standings['MassMutual East'][0]['info']['id'], standings['MassMutual East'][3]['info']['id'])
        self.update_matchup(e2, standings['MassMutual East'][1]['info']['id'], standings['MassMutual East'][2]['info']['id'])
        self.update_matchup(w1, standings['Honda West'][0]['info']['id'], standings['Honda West'][3]['info']['id'])
        self.update_matchup(w2, standings['Honda West'][1]['info']['id'], standings['Honda West'][2]['info']['id'])

    def create_matchups_round1(self, standings):
        if len(standings['Scotia North']) == 2:
            n = self._matchups['n']
            if not n["start"]:
                print(f"Create Scotia North final {standings['Scotia North'][0]['info']['abbreviation']} vs {standings['Scotia North'][1]['info']['abbreviation']}")
                self.update_matchup(n, standings['Scotia North'][0]['info']['id'], standings['Scotia North'][1]['info']['id'])
        if len(standings['Discover Central']) == 2:
            c = self._matchups['c']
            if not c["start"]:
                print(f"Create Discover Central final {standings['Discover Central'][0]['info']['abbreviation']} vs {standings['Discover Central'][1]['info']['abbreviation']}")
                self.update_matchup(c, standings['Discover Central'][0]['info']['id'], standings['Discover Central'][1]['info']['id'])
        if len(standings['MassMutual East']) == 2:
            e = self._matchups['e']
            if not e["start"]:
                print(f"Create MassMutual East final {standings['MassMutual East'][0]['info']['abbreviation']} vs {standings['MassMutual East'][1]['info']['abbreviation']}")
                self.update_matchup(e, standings['MassMutual East'][0]['info']['id'], standings['MassMutual East'][1]['info']['id'])
        if len(standings['Honda West']) == 2:
            w = self._matchups['w']
            if not w["start"]:
                print(f"Create Honda West final {standings['Honda West'][0]['info']['abbreviation']} vs {standings['Honda West'][1]['info']['abbreviation']}")
                self.update_matchup(w, standings['Honda West'][0]['info']['id'], standings['Honda West'][1]['info']['id'])

    def create_matchups_round2(self, standings):
        if len(standings["teams"]) == 4:
            sc1 = self._matchups['sc1']
            if not sc1["start"]:
                print(f"Create Stanley cup semi final #1 {standings['teams'][0]['info']['abbreviation']} vs {standings['teams'][3]['info']['abbreviation']}")
                self.update_matchup(sc1, standings['teams'][0]['info']['id'], standings['teams'][3]['info']['id'])
            sc2 = self._matchups['sc2']
            if not sc2["start"]:
                print(f"Create Stanley cup semi final #2 {standings['teams'][1]['info']['abbreviation']} vs {standings['teams'][2]['info']['abbreviation']}")
                self.update_matchup(sc2, standings['teams'][1]['info']['id'], standings['teams'][2]['info']['id'])

    def create_matchups_round3(self, standings):
        if len(standings["teams"]) == 2:
            sc = self._matchups['sc']
            if not sc["start"]:
                print(f"Create Stanley cup matchup {standings['teams'][0]['info']['abbreviation']} vs {standings['teams'][1]['info']['abbreviation']}")
                self.update_matchup(sc, standings['teams'][0]['info']['id'], standings['teams'][1]['info']['id'])
    

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

    upd = Updater2021(server)
    upd.run()
    upd.display()
