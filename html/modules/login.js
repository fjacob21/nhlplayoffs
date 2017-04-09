import React from 'react'
import { render } from 'react-dom'
var Navigation = require('react-router').Navigation;
import { Modal, Button, Input, NavDropdown, MenuItem, Alert } from 'react-bootstrap'

var Store = require('./store');

var store = new Store();

var Login = module.exports = React.createClass({
   getInitialState: function() {
         return {error: false, loaded: false, started: false};
   },
   componentDidMount: function(){
           store.load(function(data) {
                   var state = this.state;
                   state.loaded = true;
                   state.started = store.isRountStarted(1);
                   this.setState(state);
           }.bind(this),function() {
                   alert('Error!!!');
           }.bind(this));
   },
   onCreate: function(event) {
    event.preventDefault();
    this.props.history.push('/adduser')
  },
  onGuest: function(event) {
   event.preventDefault();
   var data = {psw:this.refs.psw.getValue()};
   $.ajax({
    type: 'POST',
    url: "/nhlplayoffs/api/v2.0/players/guest/login",
    data: JSON.stringify (data),
    success: function(data) {
            sessionStorage.setItem('userId', data.user);
            sessionStorage.setItem('user', 'guest');
            this.props.history.push('/main/home'); }.bind(this),
    error: function(data) {  this.setState({error: true}); }.bind(this),
    contentType: "application/json",
    dataType: 'json'
});
 },
  onLogin: function(event) {
   event.preventDefault();
   var user = this.refs.user.getValue();
   var data = {psw:this.refs.psw.getValue()};
   $.ajax({
    type: 'POST',
    url: "/nhlplayoffs/api/v2.0/players/"+user+"/login",
    data: JSON.stringify (data),
    success: function(data) {
            console.debug(data);
            sessionStorage.setItem('userId', data.user);
            sessionStorage.setItem('userEmail', data.info.email);
            sessionStorage.setItem('user', user);
            this.props.history.push('/main/home'); }.bind(this),
    error: function(data) {  this.setState({error: true}); }.bind(this),
    contentType: "application/json",
    dataType: 'json'
});

  },
  handleKeyPress: function(event) {
          if(event.charCode==13){
                   this.onLogin(event);
           }
   },
  render() {
          var err = "";
          if(this.state.error)
              err =  <Alert bsStyle="danger">Invalid user or password</Alert>;
          var create = "";
          if (this.state.loaded){
                  if (this.state.started)
                        create = <Button onClick={this.onGuest}>Guest</Button>
                  else
                        create = <Button onClick={this.onCreate}>Create</Button>

          }
    return (
            <div className="static-modal">
                    <Modal.Dialog>
                            <Modal.Header>
                                    <Modal.Title>Login</Modal.Title>
                            </Modal.Header>
                            <Modal.Body>

                                    <form onKeyPress={this.handleKeyPress}>
                                            <Input autoFocus type="user" ref="user" label="username" placeholder="Enter username" />
                                            <Input type="password" ref="psw" label="Password" />
                                    </form>

                            </Modal.Body>

                            <Modal.Footer>
                                    {err}
                                    {create}
                                    <Button type="submit" onClick={this.onLogin} bsStyle="primary">Login</Button>
                            </Modal.Footer>
                    </Modal.Dialog>
            </div>
    )
  }
})
