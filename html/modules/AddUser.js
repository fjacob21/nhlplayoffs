import React from 'react'
import { render } from 'react-dom'
var Navigation = require('react-router').Navigation;
import { Modal, Button, Input, Alert } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'


var AddUser = module.exports = React.createClass({
        getInitialState: function() {
              return {error: false, msg:""};
        },
        onCreate: function(event) {
                event.preventDefault();
                var user = this.refs.user.getValue();
                var email = this.refs.email.getValue();
                var psw = this.refs.psw.getValue();
                var cpsw = this.refs.cpsw.getValue();
                if(user == ""){
                        this.state.error = true;
                        this.state.msg = "Cannot have empty player name";
                        this.setState(this.state);
                        return;
                }
                if(psw != cpsw){
                        this.state.error = true;
                        this.state.msg = "Cannot confirm password";
                        this.setState(this.state);
                        return;
                }
                var data = {    'name':user,
                                'psw':this.refs.psw.getValue(),
                                'email':email};
                $.ajax({
                 type: 'POST',
                 url: "/nhlplayoffs/api/v2.0/players",
                 data: JSON.stringify (data),
                 success: function(data) {
                         sessionStorage.setItem('userId', data.user);
                         sessionStorage.setItem('userEmail', data.info.email);
                         sessionStorage.setItem('user', user);
                         //document.login_user={id:data.user,name:user};
                         this.props.history.push('/main/home'); }.bind(this),
                 error: function(data) {  this.setState({error: true, msg:"Cannot create player! Player already exist"}); }.bind(this),
                 contentType: "application/json",
                 dataType: 'json'
             });
        },
        onCancel: function(event) {
                event.preventDefault();
                this.props.history.push('/')
        },
        handleKeyPress: function(event) {
                if(event.charCode==13){
                         this.onCreate(event);
                 }
         },
        render() {
                var err = "";
                if(this.state.error)
                    err =  <Alert bsStyle="danger">{this.state.msg}</Alert>;
        return (
            <div className="static-modal">
                    <Modal.Dialog>
                            <Modal.Header>
                                    <Modal.Title>Login</Modal.Title>
                            </Modal.Header>
                            <Modal.Body>
                                    <form onKeyPress={this.handleKeyPress}>
                                            <Input type="user" ref="user" label="username" placeholder="Enter username" />
                                            <Input type="email" ref="email" label="Email Address" placeholder="Enter email" />
                                            <Input type="password" ref="psw" label="Password" />
                                            <Input type="password" ref="cpsw" label="confirm password" />
                                    </form>
                            </Modal.Body>

                            <Modal.Footer>
                                    {err}
                                    <Button onClick={this.onCancel}>Cancel</Button>
                                    <Button onClick={this.onCreate} bsStyle="primary">Create</Button>
                            </Modal.Footer>
                    </Modal.Dialog>
            </div>
    )
  }
})
