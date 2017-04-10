var React = require('react');
import { Modal, Button, Input, Alert } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'
import { Router, Route, Link } from 'react-router'

class UserInfo extends React.Component{

        constructor(props) {
                super(props);
                var username = "";
                var email = "";
                if(sessionStorage.user) {
                        username = sessionStorage.user;
                        email = sessionStorage.userEmail;
                }
                this.state = {email:email, username:username, error: false, msg:""};
        }

        onUpdate(event) {
                event.preventDefault();
                var user = this.state.username;
                var email = this.state.email;
                if(email == ""){
                        this.state.error = true;
                        this.state.msg = "Cannot have empty email";
                        this.setState(this.state);
                        console.debug("Cannot have empty player name");
                        return;
                }
                var data = {'email':email};

                console.debug("update user", data);
                $.ajax({
                 type: 'PUT',
                 url: "/nhlplayoffs/api/v2.0/players/"+user,
                 data: JSON.stringify (data),
                 success: function(data) {
                         this.state.error = false;
                         this.state.msg = "";
                         sessionStorage.setItem('userEmail', email);
                 }.bind(this),
                 error: function(data) {
                         this.state.error = true;
                         this.state.msg = "Cannot update user info";
                         this.setState(this.state);
                        }.bind(this),
                 contentType: "application/json",
                 dataType: 'json'
             });
        }

        onChangePsw(event) {
                event.preventDefault();
                var user = this.state.username;
                var opsw = this.refs.opsw.getValue();
                var npsw = this.refs.npsw.getValue();

                var data = { 'old_psw':opsw,
                              'new_psw': npsw};

                $.ajax({
                 type: 'POST',
                 url: "/nhlplayoffs/api/v2.0/players/"+user+"/chpsw",
                 data: JSON.stringify (data),
                 success: function(data) {
                         if (data.result) {
                                this.state.error = false;
                                this.state.msg = "";
                                this.setState(this.state);
                                console.debug("Change psw success!!!!");
                         } else {
                                this.state.error = true;
                                this.state.msg = "Cannot change password";
                                this.setState(this.state);
                                console.debug("Cannot change password");
                         }

                 }.bind(this),
                 error: function(data) {
                         this.state.error = true;
                         this.state.msg = "Cannot change password";
                         this.setState(this.state);
                         console.debug("Cannot change password");
                        }.bind(this),
                 contentType: "application/json",
                 dataType: 'json'
             });
        }

        handleEmailChange(event) {
            this.setState({email: event.target.value});
        }

        handleKeyPress(type, event){
                if(event.charCode==13){
                        if (type == 'info')
                                this.onUpdate(event);
                        if (type == 'psw')
                                this.onChangePsw(event);
                 }
        }

        render(){
                var err = "";
                if(this.state.error)
                    err =  <Alert bsStyle="danger">{this.state.msg}</Alert>;
                var username = "";
                var email = "";
                if(sessionStorage.user) {
                        username = sessionStorage.user;
                        email = sessionStorage.userEmail;
                }
                return (
                        <div className='userinfo'>

                                <form onKeyPress={this.handleKeyPress.bind(this, 'info')}>
                                        <Input type="user" readOnly label="username" placeholder="Enter username" value={this.state.username}/>
                                        <Input type="email" label="Email Address" placeholder="Enter email" value={this.state.email} onChange={this.handleEmailChange.bind(this)}/>
                                        <Button onClick={this.onUpdate.bind(this)} bsStyle="primary">Update</Button>
                                </form>

                                <form onKeyPress={this.handleKeyPress.bind(this, 'psw')}>
                                        <Input type="password" ref="opsw" label="Old Password" />
                                        <Input type="password" ref="npsw" label="New Password" />
                                        <Button onClick={this.onChangePsw.bind(this)} bsStyle="primary">Change Password</Button>
                                </form>

                                {err}
                        </div>)
        }
}

module.exports = UserInfo;
