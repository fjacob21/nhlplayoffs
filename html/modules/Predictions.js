var React = require('react');
var TeamSelector = require('./teamSelector');
import { Navbar, NavItem, NavDropdown, MenuItem, Nav, Button, DropdownButton, PageHeader, Alert } from 'react-bootstrap';
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
                                "msgstyle": {"opacity":0.0, "transition": "opacity 0s", "top": window.pageYOffset+50 },
                                "messsage": "",
                                "msgtype": "danger",
                                "predictions":store.getPredictions(sessionStorage.userId),
                                "teams":store.getTeams(true),
                                "winner":store.getWinner(sessionStorage.userId),
                                "currentround":store.currentround
                        };
                        this.setState(state);
                        this.timer = setInterval(this.tick, 60000);
                }.bind(this),function() {
                        alert('Error!!!');
                }.bind(this));
        },
        componentWillUnmount: function(){
                clearInterval(this.timer);
        },

        tick: function(){
                this.setState(this.state);
        },
        msgofftick: function(){
                this.state.msgstyle = {"opacity":0.0, "transition": "opacity 2s", "top": window.pageYOffset+50 };
                this.setState(this.state);
        },
        getInitialState: function() {
          return {predictions: [], teams:[], winner:0, currentround:0};
        },
        winnerChange: function(event) {
                if ((sessionStorage.user != 'guest' && store.isRountStarted(1)) || store.currentround==0){
                        this.setState(this.state);
                        return;
                }
                this.state.winner = event.target.value;
                this.setState(this.state);
                if (sessionStorage.user != 'guest')
                        store.setWinner(sessionStorage.userId, this.state.winner,
                                function(data){
                                        this.state.msgstyle = {"opacity":1.0, "transition": "opacity 0s", "top": window.pageYOffset+50 };
                                        this.state.msgtype = "success";
                                        this.state.messsage = "Winner prediction success";
                                        this.setState(this.state);
                                        setTimeout(this.msgofftick, 1000);
                                }.bind(this),
                                function(){
                                        this.state.msgstyle = {"opacity":1.0, "transition": "opacity 0s", "top": window.pageYOffset+50 };
                                        this.state.msgtype = "danger";
                                        this.state.messsage = "Cannot set Winner";
                                        this.setState(this.state);
                                        setTimeout(this.msgofftick, 1000);
                                }.bind(this));
        },
        predictionChange: function(event) {
                var prediction = this.state.predictions[event.target.id];
                if((sessionStorage.user != 'guest' && store.isMatchupStarted(store.getMatchup(prediction.home, prediction.away, prediction.round))) || store.currentround==0)
                        return;
                this.state.predictions[event.target.id].winner = event.target.value;
                this.setState(this.state);
                if (sessionStorage.user != 'guest')
                        store.setPrediction(sessionStorage.userId, prediction.round, prediction.home, prediction.away, prediction.winner, prediction.games,
                                function(data){
                                        this.state.msgstyle = {"opacity":1.0, "transition": "opacity 0s", "top": window.pageYOffset+50 };
                                        this.state.msgtype = "success";
                                        this.state.messsage = "Team prediction success";
                                        this.setState(this.state);
                                        setTimeout(this.msgofftick, 1000);
                                }.bind(this),
                                function(){
                                        this.state.msgstyle = {"opacity":1.0, "transition": "opacity 0s", "top": window.pageYOffset+50 };
                                        this.state.msgtype = "danger";
                                        this.state.messsage = "Cannot set predictions team";
                                        this.setState(this.state);
                                        setTimeout(this.msgofftick, 1000);
                                }.bind(this));
        },
        gamesChange: function(event) {
                var prediction = this.state.predictions[event.target.id];
                if((sessionStorage.user != 'guest' && store.isMatchupStarted(store.getMatchup(prediction.home, prediction.away, prediction.round))) || store.currentround==0)
                        return;
                this.state.predictions[event.target.id].games = Number(event.target.value);
                this.setState(this.state);
                if (sessionStorage.user != 'guest')
                        store.setPrediction(sessionStorage.userId, prediction.round, prediction.home, prediction.away, prediction.winner, prediction.games,
                                function(data){
                                        this.state.msgstyle = {"opacity":1.0, "transition": "opacity 0s", "top": window.pageYOffset+50 };
                                        this.state.msgtype = "success";
                                        this.state.messsage = "Games prediction success";
                                        this.setState(this.state);
                                        setTimeout(this.msgofftick, 1000);
                                }.bind(this),
                                function(){
                                        this.state.msgstyle = {"opacity":1.0, "transition": "opacity 0s", "top": window.pageYOffset+50 };
                                        this.state.msgtype = "danger";
                                        this.state.messsage = "Cannot set predictions games";
                                        this.setState(this.state);
                                        setTimeout(this.msgofftick, 1000);
                                }.bind(this));
        },
        render: function() {
        var teams = this.state.teams.map(function(team) {
              var id = team;
              id = id.info.id;
              var url= "https://www-league.nhlstatic.com/builds/site-core/284dc4ec70e4bee8802842e5e700157f45660a48_1457473228/images/team/logo/current/" +String(id)+ "_dark.svg";
              return (
                       <option value={team.info.id} key={team.info.id}>
                               {team.info.name}
                       </option>
              );
      });

        var predictions = this.state.predictions.map(function(prediction,i){
                var homeClass = 'btn btn-primary ';
                var awayClass = 'btn btn-primary ';
                if (prediction.winner==prediction.home)
                        homeClass += 'active predictionSel';
                else if (prediction.winner==prediction.away)
                        awayClass += 'active predictionSel';
                var homeUrl = 'https://www-league.nhlstatic.com/builds/site-core/284dc4ec70e4bee8802842e5e700157f45660a48_1457473228/images/team/logo/current/' + store.getTeam(prediction.home).info.id + '_dark.svg';
                var awayUrl = 'https://www-league.nhlstatic.com/builds/site-core/284dc4ec70e4bee8802842e5e700157f45660a48_1457473228/images/team/logo/current/' + store.getTeam(prediction.away).info.id + '_dark.svg';
                var homeTeam = store.getTeam(prediction.home);
                var awayTeam = store.getTeam(prediction.away);
                var matchup = store.getMatchup(prediction.home, prediction.away, prediction.round);
                var diffStr = 'Not available';
                if (matchup.start != '') {
                        var start  = new Date(matchup.start);
                        var now = new Date(Date.now());
                        var diff = start-now;
                        var diffDay = Math.max(0, Math.floor((start-now)/(1000*60*60*24)));
                        var diffHour = Math.max(0, Math.floor((start-now - (diffDay*(1000*60*60*24)))/(1000*60*60)));
                        var diffMin = Math.max(0, Math.floor((start-now - (diffDay*(1000*60*60*24)) - (diffHour*(1000*60*60)))/(1000*60)));
                        var dstart = start.toLocaleString();
                        diffStr = diffDay + ' days ' + diffHour+'h'+diffMin +'m';
                        if(diffDay==0 && diffHour==0 && diffMin==0)
                                diffStr = 'Started';
                }
                return (
                        <div key={i} className='prediction'>
                               <div className='round cell'>{matchup.round}</div>
                                <div className='teams cell'>
                                        <TeamSelector id={i} matchup={matchup} value={prediction.winner} onChange={this.predictionChange} store={store}/>
                                </div>
                                <div className='games cell'>
                                        <select className='form-control' value={prediction.games} id={i} onChange={this.gamesChange}>
                                                <option value={4} >4</option>
                                                <option value={5}>5</option>
                                                <option value={6}>6</option>
                                                <option value={7}>7</option>
                                        </select>
                                </div>
                                <div className='time-left cell'>
                                        {diffStr}
                                </div>

                        </div>
                );
        }.bind(this));
        var emptyPrediction = <option disabled></option>;
        if (this.state.winner == 0) {
                emptyPrediction = <option value={0}>Select a winning teams</option>;
        }
        const alertInstance = (
                <Alert bsStyle={this.state.msgtype} className='msg' style={this.state.msgstyle}>
                        {this.state.messsage}
                </Alert>
        );
        return (
                <div>
                        {alertInstance}
                        <h1>Predictions</h1>
                        <div className='predictions table table-hover'>
                                <div className='header'>
                                        <div className='round cell'>R</div>
                                        <div className='teams cell'>Winner</div>
                                        <div className='games cell'>Games</div>
                                        <div className='time-left cell'>Time left</div>

                                </div>
                                {predictions}
                        </div>
                        <PageHeader>Winner prediction</PageHeader>
                        <select className='form-control' style={{width: '300px'}} id='winner_prediction' value={this.state.winner} onChange={this.winnerChange}>
                                {emptyPrediction}
                                {teams}
                        </select>
                </div>
        );
        }
});

module.exports = Predictions;
