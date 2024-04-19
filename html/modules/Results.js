var React = require('react');
import { Navbar, NavItem, NavDropdown, MenuItem, Nav, Button, Glyphicon } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap'
import { Router, Route, Link } from 'react-router'
var Store = require('./store');

var store = new Store();

class Results extends React.Component{
        constructor(props) {
                super(props);
                this.state = {matchups:[], results: [], teams:[], winner:null, currentround:0};
        }

        componentDidMount(){
                if(!sessionStorage.user)
                        this.props.history.push('/')
                store.load(function(data) {
                        var state = this.state;
                        state.matchups = store.getMatchups(0);
                        state.matchups.sort(function(a, b){return a.round - b .round;});
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

        isFinished(){
                if (store.matchups.sc == undefined)
                        return false;
                if (store.matchups.sc.result.home_win == 4)
                    return true;
                else if (store.matchups.sc.result.away_win == 4)
                    return true;
                return false;
        }
        findPrediction(predictions, home, away){
                for (var prediction of predictions){
                        if (prediction.home == home && prediction.away == away)
                                return prediction;
                }
                return null;
        }

        render() {
                var results = this.state.results.map(function(result,i){
                                        var m = this.state.matchups.map(function(matchup, j){
                                           if(matchup.home != 0 && matchup.away != 0) {
                                                //Get player predictions
                                                var home = matchup.home;
                                                var away = matchup.away;
                                                var matchupResult = store.getMatchupResult(matchup);
                                                var predClass = '';
                                                var p = this.findPrediction(result.predictions, home, away);
                                                if(p != null){
                                                        // var predImg = '<use xlink:href="' + store.getTeamImgUrl(p.winner) + '" />';
                                                        var predImg = <img id={'img-' + p.winner} className='matchup-img' src={store.getTeamImgUrl(p.winner)} />;
                                                        if(matchupResult.winner !=0 && matchupResult.winner != p.winner){
                                                                if(matchupResult.isFinish)
                                                                        predClass = 'teamLoser';
                                                                else
                                                                        predClass = 'teamLosing';
                                                        }
                                                        return (
                                                                <th style={{width: '1%', height: '10px'}} key={j}>
                                                                        <div className={predClass} style={{width: '35px', height: '23px'}}>{predImg}</div><div>{p.games}</div>
                                                                </th>);
                                                } else{
                                                        return (
                                                                <th style={{width: '10px'}} key={j}>

                                                                </th>);
                                                }
                                             }
                                        }.bind(this));
                        var winnerClass = '';
                        var winner = <div></div>;
                        var winnerstar = <div></div>;
                        if (i==0 && this.isFinished())
                                winnerstar = <Glyphicon className='winner-star' glyph="star" />;
                        if(result.winner != 0){
                                // var predImg = '<use xlink:href="' + store.getTeamImgUrl(result.winner) + '" />';
                                var predImg = <img id={'img-' + result.winner} className='matchup-img' src={store.getTeamImgUrl(result.winner)} />;
                                winner = <img className={winnerClass} src={store.getTeamImgUrl(result.winner)} style={{width: '50px', height: 'auto'}} />
                                winner = <div style={{width: '35px', height: '23px'}}>{predImg}</div>
                        }
                        return (<tr key={i}><th className='rank'>{i+1}</th><th style={{width: '50px',verticalAlign: 'middle'}}>{result.player}</th>{m}<th style={{width: '50px',verticalAlign: 'middle'}} >{winner}</th><th style={{width: '50px',verticalAlign: 'middle'}}><div>{result.pts}{winnerstar}</div></th></tr>);
                }.bind(this));

                                var currentRound = 0;
                                var matchsHead = this.state.matchups.map(function(matchup, j){
                                    if(matchup.home != 0 && matchup.away != 0) {
                                       var roundSeparator = <th></th>;
                                        if (matchup.round != currentRound){
                                           currentRound = matchup.round;
                                        }
                                        //Get player predictions
                                        var home = matchup.home;
                                        var away = matchup.away;
                                        var homeWin = 0;
                                        var awayWin = 0;
                                        if(matchup.result != undefined){
                                                var homeWin = matchup.result.home_win;
                                                var awayWin = matchup.result.away_win;
                                        }

                                        var result = store.getMatchupResult(matchup);
                                        var homeClass = '';
                                        var awayClass = '';
                                        // var homeImg = '<use xlink:href="' + store.getTeamImgUrl(home) + '" />';
                                        // var awayImg = '<use xlink:href="' + store.getTeamImgUrl(away) + '" />';
                                        var homeImg = <img className='matchup-img' src={store.getTeamImgUrl(home)} />;
                                        var awayImg = <img className='matchup-img' src={store.getTeamImgUrl(away)} />;
                                        //<img className={homeClass} src={store.getTeamImgUrl(home)} style={{width: '100%', height: 'auto'}} />{homeWin}
                                        //<img className={awayClass} src={store.getTeamImgUrl(away)} style={{width: '100%', height: 'auto'}} />{awayWin}
                                        if(result.isFinish){
                                                if(result.winner == home)
                                                        awayClass = 'teamLoser';
                                                else
                                                        homeClass = 'teamLoser';
                                        }
                                        return (
                                                <th style={{width: '10px'}} key={j}>
                                                        <div className={homeClass} style={{width: '35px', height: '23px'}}>
                                                                {homeImg}
                                                        </div>
                                                        <div>{homeWin}</div>
                                                        <div className={awayClass} style={{width: '35px', height: '23px'}}>
                                                                {awayImg}
                                                        </div>
                                                        <div>{awayWin}</div>
                                                </th>);
                                       }
                                }.bind(this));
                return (
                        <table className='table table-hover'>
                                <thead>
                                    <tr>
                                        <th>Rank</th>
                                        <th>Player</th>
                                        {matchsHead}
                                        <th>Winner</th>
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
