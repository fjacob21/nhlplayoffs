var React = require('react');
import { Navbar, NavItem, NavDropdown, MenuItem, Nav, Button } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap'
import { Router, Route, Link } from 'react-router'

class TeamSelector extends React.Component{
        constructor(props) {
                super(props);
                this.state = {};
                this.value = this.props.value;
                this.id = this.props.id;
        }

        componentDidMount(){

        }

        homeSelect(event) {
                this.value = this.props.matchup.home;
                event.target = this;
                this.props.onChange(event);
        }

        awaySelect(event) {
                this.value = this.props.matchup.away;
                event.target = this;
                this.props.onChange(event);
        }

        render() {
                var store = this.props.store;
                var matchup = this.props.matchup;
                var homeTeam = store.getTeam(this.props.matchup.home);
                var awayTeam = store.getTeam(this.props.matchup.away);

                var homeImgStyle = 'homeimg';
                var awayImgStyle = 'awayimg';
                if (this.props.matchup.home == this.props.value)
                        homeImgStyle += " selected";
                else if (this.props.matchup.away == this.props.value)
                        awayImgStyle += " selected";

                var homeImg = <img id={'img-' + this.props.matchup.home} className='matchup-img' src={store.getTeamImgUrl(this.props.matchup.home)} />;
                homeImg = '<use xlink:href="' + store.getTeamImgUrl(this.props.matchup.home) + '" />';
                var awayImg = <img className='matchup-img' src={store.getTeamImgUrl(this.props.matchup.away)} />;
                awayImg = '<use xlink:href="' + store.getTeamImgUrl(this.props.matchup.away) + '" />';
                return (
                        <div className='team-selector'>
                                <div className={homeImgStyle} onClick={this.homeSelect.bind(this)}><div className='team-rank'>{homeTeam.standings.divisionRank}</div> <svg viewBox="0 0 5 5">
                                        <svg dangerouslySetInnerHTML={{__html: homeImg }} />
                                </svg> </div>
                                <div className='results'>{matchup.season.home_win + " - " + matchup.season.away_win}</div>
                                <div className={awayImgStyle} onClick={this.awaySelect.bind(this)}><div className='team-rank'>{awayTeam.standings.divisionRank}</div> <svg viewBox="0 0 5 5">
                                        <svg dangerouslySetInnerHTML={{__html: awayImg }} />
                                </svg> </div>
                        </div>
                );
        }
}

module.exports = TeamSelector;
