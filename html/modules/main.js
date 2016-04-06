var App = require('./App');
var Home = require('./Home');
var About = require('./About');
var Login = require('./login');
var AddUser = require('./AddUser');
var Results = require('./Results');
var Predictions = require('./Predictions');


import React from 'react'
import { render } from 'react-dom'
import { Router, Route, Link } from 'react-router'

render((
  <Router>
    <Route path="/" component={Login} />
    <Route path="/adduser" component={AddUser} />
    <Route path="/main" component={App}>
      <Route path="/main/home" component={Home} />
      <Route path="/main/about" component={About} />
      <Route path="/main/predictions" component={Predictions} />
      <Route path="/main/results" component={Results} />
    </Route>
  </Router>
), document.body)
