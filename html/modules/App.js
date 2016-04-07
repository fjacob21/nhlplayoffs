import React from 'react'
import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'
import { Nav, Navbar, NavItem, NavDropdown, MenuItem } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'

const App = React.createClass({
  getInitialState: function() {
    return {navExpanded: false};
  },
  onLogout: function(event)  {
          event.preventDefault();
          this.props.history.push('/')
        },
  onNavItemClick: function(event)  {
    this.setState({ navExpanded: false });
        },
  onNavbarToggle: function(event)  {
    this.setState({ navExpanded: ! this.state.navExpanded });
        },
        render() {
        var username = document.login_user.name;
        return (
                <div>
                         <Navbar inverse expanded={ this.state.navExpanded } onToggle={ this.onNavbarToggle } >
                                 <Navbar.Header>
                                         <Navbar.Brand>
                                                 <LinkContainer to="/main/home">
                                                         <a href="#">
                                                                 <table><tr><th>
                                                                 <img width="30" height="30" src="http://cdn.nhle.com/projects/ice3-ui/com.nhl.ice3.ui.t5.components/GlobalPageImports/images/nhl_shield.png"/>
                                                                 </th><th>NHL Playoffs pool</th></tr></table>
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
                                                 <NavItem eventKey={5} onClick={ this.onLogout }>{username} Logout</NavItem>
                                         </Nav>
                                 </Navbar.Collapse>
                         </Navbar>
                         {this.props.children}
                 </div>
    )
  }
})

module.exports = App;
