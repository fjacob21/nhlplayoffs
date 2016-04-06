import React from 'react'
import { render } from 'react-dom'
var Navigation = require('react-router').Navigation;
import { Modal, Button, Input, NavDropdown, MenuItem } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'


var AddUser = module.exports = React.createClass({
  onCreate: function(event) {
    event.preventDefault();
    this.props.history.push('/main')
  },
  onCancel: function(event) {
   event.preventDefault();
   this.props.history.push('/')
  },
  render() {
    return (
            <div className="static-modal">
                    <Modal.Dialog>
                            <Modal.Header>
                                    <Modal.Title>Login</Modal.Title>
                            </Modal.Header>
                            <Modal.Body>
                                    <form>
                                            <Input type="user" label="username" placeholder="Enter username" />
                                            <Input type="email" label="Email Address" placeholder="Enter email" />
                                            <Input type="password" label="Password" />
                                            <Input type="password" label="confirm password" />
                                    </form>
                            </Modal.Body>

                            <Modal.Footer>
                                    <Button onClick={this.onCreate}>Create</Button>
                                    <Button onClick={this.onCancel}bsStyle="primary">Cancel</Button>
                            </Modal.Footer>
                    </Modal.Dialog>
            </div>
    )
  }
})
