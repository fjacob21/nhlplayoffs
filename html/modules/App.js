import React from 'react'
import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'
import { Nav, Navbar, NavItem, NavDropdown, MenuItem } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'

const App = React.createClass({
  componentDidMount: function(){
        if(!sessionStorage.user)
                this.props.history.push('/')
  },
  getInitialState: function() {
    return {navExpanded: false};
  },
  onLogout: function(event)  {
          event.preventDefault();
          sessionStorage.clear();
          this.props.history.push('/')
        },
  onNavItemClick: function(event)  {
    this.setState({ navExpanded: false });
        },
  onNavbarToggle: function(event)  {
    this.setState({ navExpanded: ! this.state.navExpanded });
        },
        render() {
        var username = "";
        if(sessionStorage.user)
                username = sessionStorage.user;
        var userinfoLink = "";
        if (username != 'guest')
                userinfoLink = <LinkContainer to="/main/userinfo"><NavItem eventKey={5} onClick={ this.onNavItemClick }>{username}</NavItem></LinkContainer>
        return (
                <div className='app'>
                         <Navbar fixedTop={true} inverse expanded={ this.state.navExpanded } onToggle={ this.onNavbarToggle } >
                                 <Navbar.Header>
                                         <Navbar.Brand>
                                                 <LinkContainer to="/main/home">
                                                         <a href="#">
                                                                <table>
                                                                        <tbody>
                                                                        <tr>
                                                                                <th><img width="30" height="30" src="http://cdn.nhle.com/projects/ice3-ui/com.nhl.ice3.ui.t5.components/GlobalPageImports/images/nhl_shield.png"/></th>
                                                                                <th>NHL Playoffs pool</th>
                                                                        </tr>
                                                                        </tbody>
                                                                </table>
                                                         </a>
                                                 </LinkContainer>
                                         </Navbar.Brand>
                                         <Navbar.Toggle />
                                 </Navbar.Header>
                                 <Navbar.Collapse>
                                         <Nav>
                                                 <LinkContainer to="/main/home"><NavItem eventKey={1} onClick={ this.onNavItemClick }>Home</NavItem></LinkContainer>
                                                 <LinkContainer to="/main/predictions"><NavItem eventKey={2} onClick={ this.onNavItemClick }>Predictions</NavItem></LinkContainer>
                                                 <LinkContainer to="/main/results"><NavItem eventKey={3} onClick={ this.onNavItemClick }>Results</NavItem></LinkContainer>
                                         </Nav>
                                         <Nav pullRight>
                                                 <LinkContainer to="/main/about"><NavItem eventKey={4} onClick={ this.onNavItemClick }>About</NavItem></LinkContainer>
                                                 {userinfoLink}
                                                 <NavItem eventKey={6} onClick={ this.onLogout }>{username} Logout</NavItem>
                                         </Nav>
                                 </Navbar.Collapse>
                         </Navbar>
                         {this.props.children}
                 </div>
    )
  }
})

module.exports = App;
