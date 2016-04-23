var React = require('react');
import { Navbar, NavItem, NavDropdown, MenuItem, Nav } from 'react-bootstrap';
var Store = require('./store');

var store = new Store();

class GameInfo extends React.Component{
        constructor(props) {
                super(props);
        }

        render(){
                return (
                        <div className='matchup-table'>
                                <div className='matchup-row'>
                                        <div className='matchup-cell'><img src={store.getTeamImgUrl(this.props.matchup.home.team.id)} style={{width: '100%', height: 'auto'}}/></div>
                                        <div className='matchup-cell'>VS</div>
                                        <div className='matchup-cell'><img src={store.getTeamImgUrl(this.props.matchup.away.team.id)} style={{width: '100%', height: 'auto'}}/></div>
                                </div>
                                <div className='matchup-row'><div>Last game</div></div>
                        </div>
                )
        }
}

class Home extends React.Component{
        constructor(props) {
                super(props);
                this.state = {matchups:{}, currentround:0};
        }

        componentDidMount(){
                if(!sessionStorage.user)
                        this.props.history.push('/')
                // store.load(function(data) {
                //         var state = this.state;
                //         state.matchups = store.matchups;
                //         state.currentround = store.currentround;
                //         store.loadResults(sessionStorage.userId, function(data) {
                //                 var state = this.state;
                //                 state.results = store.results;
                //                 this.setState(state);
                //         }.bind(this),function() {
                //                 alert('Error!!!');
                //         }.bind(this));
                // }.bind(this),function() {
                //         alert('Error!!!');
                // }.bind(this));
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

                return (
                    <div>
                            <div>Welcome to the 2016 NHL playoffs pool 🏒🏒🏒</div>
                    </div>
                )
        }
}

module.exports = Home;
