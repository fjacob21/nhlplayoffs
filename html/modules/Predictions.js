var React = require('react');
import { Navbar, NavItem, NavDropdown, MenuItem, Nav, Button, DropdownButton, PageHeader } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap'
import { Router, Route, Link } from 'react-router'
var Store = require('./store');

var store = new Store();

var Predictions = React.createClass({
        componentDidMount: function(){
                if(!sessionStorage.user)
                        this.props.history.push('/')
                store.load(function(data) {
                        var state = {
                                "predictions":store.getPredictions(sessionStorage.userId),
                                "teams":store.getTeams(),
                                "winner":store.getWinner(sessionStorage.userId),
                                "currentround":store.currentround
                        };
                        this.setState(state);
                }.bind(this),function() {
                        alert('Error!!!');
                }.bind(this));
        },
        getInitialState: function() {
          return {predictions: [], teams:[], winner:null, currentround:0};
        },
        winnerChange: function(event) {
            this.state.winner = event.target.value;

            store.setWinner(sessionStorage.userId, this.state.winner, function(data){this.setState(this.state);}.bind(this), function(){alert('Error!!!');}.bind(this));
          },
        predictionChange: function(event) {
                this.state.predictions[event.target.id].winner = Number(event.target.value);
                this.setState(this.state);
                var prediction = this.state.predictions[event.target.id];
                store.setPrediction(sessionStorage.userId, prediction.round, prediction.home, prediction.away, prediction.winner, prediction.games, function(data){}.bind(this), function(){alert('Error!!!');}.bind(this));
        },
        gamesChange: function(event) {
                this.state.predictions[event.target.id].games = Number(event.target.value);
                this.setState(this.state);
                var prediction = this.state.predictions[event.target.id];
                store.setPrediction(sessionStorage.userId, prediction.round, prediction.home, prediction.away, prediction.winner, prediction.games, function(data){}.bind(this), function(){alert('Error!!!');}.bind(this));
        },
        render: function() {
        var teams = this.state.teams.map(function(team) {
              var id = team;
              id = id.team.id;
              var url= "https://www-league.nhlstatic.com/builds/site-core/284dc4ec70e4bee8802842e5e700157f45660a48_1457473228/images/team/logo/current/" +String(id)+ "_dark.svg";
              return (
                       <option value={team.team.id} key={team.team.id}>
                               {team.team.name}
                       </option>
              );
      });

        var predictions = this.state.predictions.map(function(prediction,i){
                var homeClass = 'btn btn-primary ';
                var awayClass = 'btn btn-primary ';
                if (prediction.winner==prediction.home)
                        homeClass += 'active';
                else if (prediction.winner==prediction.away)
                        awayClass += 'active';
                var homeUrl = 'https://www-league.nhlstatic.com/builds/site-core/284dc4ec70e4bee8802842e5e700157f45660a48_1457473228/images/team/logo/current/' + store.getTeam(prediction.home).team.id + '_dark.svg';
                var awayUrl = 'https://www-league.nhlstatic.com/builds/site-core/284dc4ec70e4bee8802842e5e700157f45660a48_1457473228/images/team/logo/current/' + store.getTeam(prediction.away).team.id + '_dark.svg';
                return (
                        <tr key={i}>
                                <th>
                                        <div  data-toggle='buttons'>
                                                <label className={homeClass} data-value={prediction.home} style={{width:'200px'}}>
                                                        <img style={{width: '50px'}} src={homeUrl} />
                                                        <input type="radio" name={'predcit' + String(i)}
                                                           id={i}
                                                           value={prediction.home}
                                                           checked={prediction.winner==prediction.home}
                                                           onChange={this.predictionChange} />{store.getTeam(prediction.home).team.name}
                                                </label>
                                                <label className={awayClass} data-value={prediction.away} style={{width:'200px'}}>
                                                        <img style={{width: '50px'}} src={awayUrl} />
                                                        <input type="radio" name={'predcit' + String(i)}
                                                           value={prediction.away}
                                                           id={i}
                                                           checked={prediction.winner==prediction.away}
                                                           onChange={this.predictionChange} />{store.getTeam(prediction.away).team.name}
                                                </label>
                                        </div>
                                </th>
                                <th>
                                        <select className='form-control' value={prediction.games} id={i} onChange={this.gamesChange}>
                                                <option value={4} >4</option>
                                                <option value={5}>5</option>
                                                <option value={6}>6</option>
                                                <option value={7}>7</option>
                                        </select>
                                </th>
                        </tr>
                );
        }.bind(this));
        return (
                <div>
                        <PageHeader>Round {this.state.currentround} <small>predictions</small></PageHeader>
                        <table className='table table-hover'>
                                <thead>
                                    <tr>
                                        <th>Winning team</th>
                                        <th>Number of games</th>
                                    </tr>
                                </thead>
                                <tbody className="list-group">
                                {predictions}
                        </tbody>
                        </table>
                        <PageHeader>Winner prediction</PageHeader>
                        <select className='form-control' style={{width: '300px'}} id='winner_prediction' value={this.state.winner} onChange={this.winnerChange}>
                                {teams}
                        </select>
                </div>
        );
        }
});

module.exports = Predictions;
