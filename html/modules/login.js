import React from 'react'
import { render } from 'react-dom'
var Navigation = require('react-router').Navigation;
import { Modal, Button, Input, NavDropdown, MenuItem, Alert } from 'react-bootstrap'

var Login = module.exports = React.createClass({
   getInitialState: function() {
         return {error: false};
   },
   onCreate: function(event) {
    event.preventDefault();
    this.props.history.push('/adduser')
  },
  onLogin: function(event) {
   event.preventDefault();
   var user = this.refs.user.getValue();
   var data = {psw:this.refs.psw.getValue()};
   $.ajax({
    type: 'POST',
    url: "http://localhost:5000/nhlplayoffs/api/v2.0/players/"+user+"/login",
    data: JSON.stringify (data),
    success: function(data) {  document.login_user={id:data.user,name:user};this.props.history.push('/main'); }.bind(this),
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
                                    <Button onClick={this.onCreate}>Create</Button>
                                    <Button type="submit" onClick={this.onLogin} bsStyle="primary">Login</Button>
                            </Modal.Footer>
                    </Modal.Dialog>
            </div>
    )
  }
})
