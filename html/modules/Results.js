var React = require('react');
import { Navbar, NavItem, NavDropdown, MenuItem, Nav, Button } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap'
import { Router, Route, Link } from 'react-router'
var Store = require('./store');

var store = new Store();

class Results extends React.Component{
        constructor(props) {
                super(props);
                this.state = {matchups:{}, results: [], teams:[], winner:null, currentround:0};
        }

        componentDidMount(){
                if(!sessionStorage.user)
                        this.props.history.push('/')
                store.load(function(data) {
                        var state = this.state;
                        state.matchups = store.matchups;
                        state.teams = store.getTeams();
                        state.winner =store.getWinner(sessionStorage.userId);
                        state.currentround = store.currentround;
                        store.loadResults(sessionStorage.userId, function(data) {
                                var state = this.state;
                                state.results = store.results;
                                state.results.sort(this.compareResult);
                                this.setState(state);
                        }.bind(this),function() {
                                alert('Error!!!');
                        }.bind(this));
                }.bind(this),function() {
                        alert('Error!!!');
                }.bind(this));
        }

        compareResult(a,b) {
                if(a.pts > b.pts)
                        return -1;
                else if(a.pts < b.pts)
                        return 1;
                else {
                        if(a.victories.games_count > b.victories.games_count)
                                return -1;
                        else if(a.victories.games_count < b.victories.games_count)
                                return 1;
                        else {
                                if(a.player.toLowerCase() > b.player.toLowerCase())
                                        return 1;
                                else
                                        return -1;
                        }
                }
        }

        findPrediction(predictions, home, away){
                for (var prediction of predictions){
                        if (prediction.home == home && prediction.away == away)
                                return prediction;
                }
                return null;
        }

        render() {
                var rounds=[1,2,3,4];
                var results = this.state.results.map(function(result,i){
                        var t = rounds.map(function(d,i){
                                if(this.state.matchups[i] != undefined){
                                        var m = this.state.matchups[i].map(function(matchup, j){
                                                //Get player predictions
                                                var home = matchup.home.team.id;
                                                var away = matchup.away.team.id;
                                                var matchupResult = store.getMatchupResult(matchup);
                                                var predClass = '';
                                                var p = this.findPrediction(result.predictions, home, away);
                                                if(p != null){
                                                        if(matchupResult.winner !=0 && matchupResult.winner != p.winner){
                                                                if(matchupResult.isFinish)
                                                                        predClass = 'teamLoser';
                                                                else
                                                                        predClass = 'teamLosing';
                                                        }
                                                        return (
                                                                <th style={{width: '10px'}} key={j}>
                                                                        <div><img className={predClass} src={store.getTeamImgUrl(p.winner)} style={{width: '100%', height: 'auto'}}/></div><div>{p.games}</div>
                                                                </th>);
                                                } else{
                                                        return (
                                                                <th style={{width: '10px'}} key={j}>

                                                                </th>);
                                                }
                                        }.bind(this));
                                }
                                return m;
                        }.bind(this));
                        var winnerClass = '';
                        var winner = <div></div>;
                        if(result.winner != 0)
                                winner = <img className={winnerClass} src={store.getTeamImgUrl(result.winner)} style={{width: '50px', height: 'auto'}} />
                        return (<tr key={i}><th style={{width: '50px',verticalAlign: 'middle'}}>{result.player}</th>{t}<th style={{width: '50px',verticalAlign: 'middle'}} >{winner}</th><th style={{width: '50px',verticalAlign: 'middle'}}>{result.pts}</th></tr>);
                }.bind(this));

                var matchsHead = rounds.map(function(d,i){
                        if(this.state.matchups[i] != undefined){
                                var m = this.state.matchups[i].map(function(matchup, j){
                                        //Get player predictions
                                        var home = matchup.home.team.id;
                                        var away = matchup.away.team.id;
                                        var homeWin = 0;
                                        var awayWin = 0;
                                        if(matchup.result != undefined){
                                                var homeWin = matchup.result.home_win;
                                                var awayWin = matchup.result.away_win;
                                        }

                                        var result = store.getMatchupResult(matchup);
                                        var homeClass = '';
                                        var awayClass = '';
                                        if(result.isFinish){
                                                if(result.winner == home)
                                                        awayClass = 'teamLoser';
                                                else
                                                        homeClass = 'teamLoser';
                                        }
                                        return (
                                                <th style={{width: '10px'}} key={j}>
                                                        <img className={homeClass} src={store.getTeamImgUrl(home)} style={{width: '100%', height: 'auto'}} />{homeWin}
                                                        <img className={awayClass} src={store.getTeamImgUrl(away)} style={{width: '100%', height: 'auto'}} />{awayWin}
                                                </th>);
                                }.bind(this));
                        }
                        return m;
                }.bind(this));
                return (
                        <table className='table table-hover'>
                                <thead>
                                    <tr>
                                        <th>Player</th>
                                        {matchsHead}
                                        <th style={{width: '10px'}}>Winner</th>
                                        <th>Pts</th>
                                    </tr>
                                </thead>
                                <tbody className="list-group">
                                        {results}
                                </tbody>
                        </table>
                );
        }
}

module.exports = Results;
