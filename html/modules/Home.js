var React = require('react');
import { Navbar, NavItem, NavDropdown, MenuItem, Nav, Glyphicon, Modal, OverlayTrigger, popover, tooltip, Button } from 'react-bootstrap';
var Store = require('./store');

var store = new Store();

class Line extends React.Component{
        constructor(props) {
                super(props);
        }

        render(){
                var dx = this.props.dx;
                var dy = this.props.dy;
                var className = "";
                if (dx == 0 && dy==1)
                        className = "rline";
                else if (dx==0 && dy==-1)
                        className = "lline";
                else if (dx==1 && dy==1)
                        className = "right-top-corner";
                else if (dx==1 && dy==-1)
                        className = "right-bottom-corner";
                else if (dx==-1 && dy==1)
                        className = "left-top-corner";
                else if (dx==-1 && dy==-1)
                        className = "left-bottom-corner";

                return (<div className={className}></div>)
        }
}

class Winner extends React.Component{
        constructor(props) {
                super(props);
        }

        render(){
                var winner = <img className='winner-img' src={store.getTeamImgUrl(this.props.winner)} />;
                return (
                        <div className='winner'>
                                <img className='scimg' src='https://nhl.bamcontent.com/images/logos/league/2016_Playoffs_English_Primary_WebBracketVersion.svg'></img>
                                {winner}
                        </div>)
        }
}

class GameInfo extends React.Component{
        constructor(props) {
                super(props);
                this.state = {showModal: false};
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
               return "not started";

              var lastGame = this.props.matchup.schedule[i-1];
              if (lastGame.teams.home.score > lastGame.teams.away.score){
                 last =  lastGame.teams.home.team.abbreviation + " win " + lastGame.teams.home.score + "-" + lastGame.teams.away.score;
              }
              else {
                 last = lastGame.teams.away.team.abbreviation + " win " + lastGame.teams.away.score + "-" + lastGame.teams.home.score;
              }
            }
            return last;
        }

        onTouch(event){
           event.preventDefault();
           this.setState({ showModal: true });
        }

         close() {
          this.setState({ showModal: false });
         }

        render(){
                var homeImg = <Glyphicon className='matchup-img' glyph="question-sign" />;
                var awayImg = <Glyphicon className='matchup-img' glyph="question-sign" />;
                var nextGame = this.findNextMatch(this.props.matchup);
                var LastGame = this.findLastMatch(this.props.matchup);

                //console.debug(this.props.matchup.schedule);
                if (this.props.matchup.home != 0)
                  homeImg = <img className='matchup-img' src={store.getTeamImgUrl(this.props.matchup.home)} />;
                if (this.props.matchup.away != 0)
                  awayImg = <img className='matchup-img' src={store.getTeamImgUrl(this.props.matchup.away)} />;
                return (
                        <div className='matchup' onTouchStart={this.onTouch.bind(this)} onClick={this.onTouch.bind(this)}>
                           <div className='teams'>
                                   <div className='matchup-cell'>{homeImg}</div>
                                   <div className='matchup-result matchup-cell'><div>{this.props.matchup.result.home_win} - {this.props.matchup.result.away_win}</div><div>...</div></div>
                                   <div className='matchup-cell'>{awayImg}</div>
                           </div>

                              <Modal show={this.state.showModal} onHide={this.close.bind(this)}>
                                  <Modal.Header closeButton>
                                    <Modal.Title>Details</Modal.Title>
                                  </Modal.Header>
                                  <Modal.Body className='matchup'>
                                  <div className='teams'>
                                      <div className='matchup-cell'>{homeImg}</div>
                                      <div className='modal-result matchup-cell'>{this.props.matchup.result.home_win} - {this.props.matchup.result.away_win}</div>
                                      <div className='matchup-cell'>{awayImg}</div>
                                  </div>
                                  <div className='info'>
                                          <div className='next'>
                                                 <div className='matchup-cell'>Next: </div>
                                                 <div className='matchup-cell'>{nextGame}</div>
                                          </div>
                                          <div className='last'>
                                                 <div className='matchup-cell'>Last: </div>
                                                 <div className='matchup-cell'>{LastGame}</div>
                                          </div>
                                  </div>
                                  </Modal.Body>
                                  <Modal.Footer>
                                    <Button onClick={this.close.bind(this)}>Close</Button>
                                  </Modal.Footer>
                             </Modal>
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
                if (root.left != null){
                  //Insert lines
                  var dx = dx;
                  var dy = (root.round-1);
                  var py = y;
                  for (var i=0;i<dy-1;i++){
                          py--;
                          display[py][x] = [0,dx];
                  }
                  py--;
                  display[py][x] = [dx,1];
                  walk_matchup_tree(root.left, x+dx, y-(root.round-1), dx);
                }
                if (root.right != null) {
                        var dx = dx;
                        var dy = (root.round-1);
                        var py = y;
                        for (var i=0;i<dy-1;i++){
                              py++;
                              display[py][x] = [0,dx];
                        }
                        py++;
                        display[py][x] = [dx,-1];
                        walk_matchup_tree(root.right, x+dx, y+(root.round-1), dx);
                }
            }
            display[2][3] = 'sc';
            walk_matchup_tree(this.state.matchups.w, 2, 3, -1);
            walk_matchup_tree(this.state.matchups.e, 4, 3, 1);

            if (this.state.matchups.sc.result.home_win == 4)
                display[0][3] = this.state.matchups.sc.home;
            else if (this.state.matchups.sc.result.away_win == 4)
                display[0][3] = this.state.matchups.sc.away;
            var result = display.map(function (row, y){
               var r = row.map(function(cell, x){
                  if (cell == '')
                     return (<div className='cell' key={x}><div></div></div>);
                  else if (typeof(cell) == 'object')
                        return (<div className='cell' key={x}><Line dx={cell[0]} dy={cell[1]} /></div>);
                  else if (typeof(cell) == 'number')
                        return (<div className='cell' key={x}><Winner winner={cell} /></div>);
                  return (<div className='cell' key={x}><GameInfo matchup={this.state.matchups[cell]}/></div>);
                  //return (<div className='cell' key={x}>{x}</div>);
               }.bind(this));
               return (<div className='row' key={y}>{r}</div>);
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
                    <div className='home'>
                            <div>Welcome to the 2016 NHL playoffs pool 🏒🏒🏒</div>
                            <div className='matchups'> {tree}</div>
                    </div>
                )
        }
}

module.exports = Home;
