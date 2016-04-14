var React = require('react');
import { Navbar, NavItem, NavDropdown, MenuItem, Nav, Button } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap'
import { Router, Route, Link } from 'react-router'
var Store = require('./store');

var store = new Store();

class Results extends React.Component{
        constructor(props) {
                super(props);
                this.state = {matchups:{},results: [], teams:[], winner:null, currentround:0};
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
                                this.setState(state);
                        }.bind(this),function() {
                                alert('Error!!!');
                        }.bind(this));
                }.bind(this),function() {
                        alert('Error!!!');
                }.bind(this));


        }

        render() {
                var rounds=[1,2,3,4];
                var results = this.state.results.map(function(result,i){
                        var t = rounds.map(function(d,i){
                                if(this.state.matchups[i] != undefined){
                                        var m = this.state.matchups[i].map(function(matchup){
                                                //Get player predictions
                                                return (<th>{matchup.home.team.name}</th>);
                                        }.bind(this));
                                }
                                return m;
                        }.bind(this));

                        return (<tr><th style={{width: '50px'}}>{result.player}</th><th style={{width: '50px'}}>{result.pts}</th></tr>);
                }.bind(this));
                console.debug(results);
                return (
                        <table className='table table-hover'>
                                <thead>
                                    <tr>
                                        <th>Player</th>
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
