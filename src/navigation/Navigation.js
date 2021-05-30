import React from 'react';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Nav from 'react-bootstrap/Nav';

class Navigation extends React.Component {

  render(){



    return (
      <Navbar bg="light" expand="lg">
        <Navbar.Brand href="/">Chromebook Tracker</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="mr-auto">
            <Nav.Link href="/chromebook_parts/">Home</Nav.Link>

            <NavDropdown title="Helper Tools" id="basic-nav-dropdown">
              <NavDropdown.Item href="/chromebook_parts/inventoryManagement">Manage Inventory</NavDropdown.Item>
              <NavDropdown.Item href="/chromebook_parts/resolveModelFromPart">Find model From Part Number</NavDropdown.Item>
              <NavDropdown.Divider />

            </NavDropdown>

          </Nav>
        </Navbar.Collapse>
      </Navbar>
    );
  }
}

export default Navigation;
