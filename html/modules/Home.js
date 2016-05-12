var React = require('react');
import { Navbar, NavItem, NavDropdown, MenuItem, Nav, Glyphicon } from 'react-bootstrap';
var Store = require('./store');

var store = new Store();

class GameInfo extends React.Component{
        constructor(props) {
                super(props);
        }

        findNextMatch(matchup){
           if (matchup.result.home_win == 4 || matchup.result.away_win == 4)
            return "Terminated";

            this.props.matchup.schedule.sort(function(a,b){
               var a = new Date(a.gameDate);
               var b = new Date(b.gameDate);
               return a<b ? -1 : a>b ? 1 : 0;
            });
            var next = "";
            if (this.props.matchup.schedule.length > 0){
               var now = new Date(Date.now());
               for(var i=0;i<this.props.matchup.schedule.length;i++){
                  var gameDate = new Date(this.props.matchup.schedule[i].gameDate);
                  if (gameDate > now)
                     break;
               }

              if (i == 7)
                return "In progress";
              next = new Date(this.props.matchup.schedule[i].gameDate);
              next = next.toLocaleString();
            }
            return next;
        }

        findLastMatch(matchup){
            this.props.matchup.schedule.sort(function(a,b){
               var a = new Date(a.gameDate);
               var b = new Date(b.gameDate);
               return a<b ? -1 : a>b ? 1 : 0;
            });
            var last = "";
            if (this.props.matchup.schedule.length > 0){
               var now = new Date(Date.now());
               for(var i=0;i<this.props.matchup.schedule.length;i++){
                  var gameDate = new Date(this.props.matchup.schedule[i].gameDate);
                  if (gameDate > now)
                     break;
               }
              if (i == 0)
               return "not stated";

              var lastGame = this.props.matchup.schedule[i-1];
              if (lastGame.teams.home.score > lastGame.teams.away.score){
                 last = lastGame.teams.home.team.abbreviation + " win " + lastGame.teams.home.score + "-" + lastGame.teams.away.score;
              }
              else {
                 last = lastGame.teams.away.team.abbreviation + " win " + lastGame.teams.away.score + "-" + lastGame.teams.home.score;
              }
            }
            return last;
        }

        render(){
                var homeImg = <Glyphicon glyph="question-sign" style={{width: '50px', height: 'auto'}}/>;
                var awayImg = <Glyphicon glyph="question-sign" style={{width: '50px', height: 'auto'}}/>;
                var nextGame = this.findNextMatch(this.props.matchup);
                var LastGame = this.findLastMatch(this.props.matchup);

                //console.debug(this.props.matchup.schedule);
                if (this.props.matchup.home != 0)
                  homeImg = <img src={store.getTeamImgUrl(this.props.matchup.home)} style={{width: '50px', height: 'auto'}}/>;
                if (this.props.matchup.away != 0)
                  awayImg = <img src={store.getTeamImgUrl(this.props.matchup.away)} style={{width: '50px', height: 'auto'}}/>;
                return (
                        <div className='matchup'>
                           <div className='matchup-table'>
                                   <div className='matchup-row'>
                                           <div className='matchup-cell'>{homeImg}</div>
                                           <div className='matchup-cell'>{this.props.matchup.result.home_win}</div>
                                           <div className='matchup-cell'>-</div>
                                           <div className='matchup-cell'>{this.props.matchup.result.away_win}</div>
                                           <div className='matchup-cell'>{awayImg}</div>
                                   </div>
                           </div>
                           <div className='matchup-table'>
                                   <div className='matchup-row'>
                                           <div className='matchup-cell'>Next: </div>
                                           <div className='matchup-cell'>{nextGame}</div>
                                   </div>
                                   <div className='matchup-row'>
                                           <div className='matchup-cell'>Last: </div>
                                           <div className='matchup-cell'>{LastGame}</div>
                                   </div>
                           </div>
                        </div>
                )
        }
}

class Home extends React.Component{
        constructor(props) {
                super(props);
                this.state = {"matchups":{}, "currentround":0};
        }

        componentDidMount(){
                if(!sessionStorage.user)
                        this.props.history.push('/')
                store.load(function(data) {
                        var state = this.state;
                        state.matchups = store.matchups;
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

        display() {
             //console.debug(this.state.matchups);
             if(this.state.matchups.w == undefined)
               return;
             var nb_round = 4;
             var width = (nb_round * 2) - 1;
             var heigh = Math.pow(2,(nb_round-1)) -1;
             var display = [];
             for(var x=0;x<width;x++) {
                display[x] = [];
                for(var y=0;y<heigh;y++) {

                  display[x][y] = '';
               }
            }
            function walk_matchup_tree(root, x, y, dx){
                display[y][x] = root.id;
                if (root.left != null)
                  walk_matchup_tree(root.left, x+dx, y-(root.round-1), dx);
                if (root.right != null)
                  walk_matchup_tree(root.right, x+dx, y+(root.round-1), dx);
            }
            display[2][3] = 'sc';
            walk_matchup_tree(this.state.matchups.w, 2, 3, -1);
            walk_matchup_tree(this.state.matchups.e, 4, 3, 1);

            var result = display.map(function (row, y){
               var r = row.map(function(cell, x){
                  if (cell == '')
                     return (<th key={x}></th>);
                  return (<th key={x}><GameInfo matchup={this.state.matchups[cell]}/></th>);
               }.bind(this));
               return (<tr key={y}>{r}</tr>);
            }.bind(this));
            return result;
        }

        render() {
                // var rounds=[1,2,3,4];
                // var matchups = rounds.map(function(d,i){
                //         if(this.state.matchups[i] != undefined){
                //                 var m = this.state.matchups[i].map(function(matchup, j){
                //                         return (<GameInfo matchup={matchup} />);
                //                 }.bind(this));
                //         }
                //         return m;
                // }.bind(this));
                var tree = this.display();
                return (
                    <div >
                            <div>Welcome to the 2016 NHL playoffs pool 🏒🏒🏒</div>
                            <center><table className='matchup-tree'> <tbody>{tree}</tbody></table></center>
                    </div>
                )
        }
}

module.exports = Home;
