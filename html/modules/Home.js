var React = require('react');
import { Navbar, NavItem, NavDropdown, MenuItem, Nav } from 'react-bootstrap';

const Home = React.createClass({
  render() {
    return <table id="table">
    <thead>
    <tr>
        <th data-field="name">Name</th>
        <th data-field="stargazers_count">Stars</th>
        <th data-field="forks_count">Forks</th>
        <th data-field="description">Description</th>
    </tr>
    </thead>
</table>
  }
})

module.exports = Home;
