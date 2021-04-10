var React = require('react');
import { Navbar, NavItem, NavDropdown, MenuItem, Nav, Button } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap'
import { Router, Route, Link } from 'react-router'

var About = React.createClass({
  render: function() {
    return (
      <div>
              <div className="container theme-showcase" role="main" id="about">
                  <div className="well">
                      <p>
                          NHL Playoffs pool V2.7 <br/>
                          This is website to manage the unofficial NHL playoffs pool.
                      </p>
                  </div>
              </div>
              <div className="container theme-showcase" role="main" id="contact">
                  <table>
                      <tr style={{height:'2px'}}><th style={{backgroundColor:'red'}}></th><th style={{backgroundColor:'orange'}}></th><th style={{backgroundColor:'green'}}></th><th style={{backgroundColor:'purple'}}></th></tr>
                      <tr><th>Frederic Jacob Ing. </th><th>| Hacker 🐎 </th><th>| <a href="mailto:fjacob21@hotmail.com">fjacob21@hotmail.com </a></th><th>|<a href="https://github.com/fjacob21/nhlplayoffs" target="_blank">GitHub </a></th></tr>
                  </table>
                  <br/>
                  <span className="copyright">&copy;Frederic Jacob Ing.</span>
              </div>
      </div>
    );
  }
});

module.exports = About;
