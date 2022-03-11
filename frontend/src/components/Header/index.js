import React from 'react'
import { Navbar, Nav } from 'react-bootstrap'
import logo from './logo.png';
import {Link} from 'react-router-dom'


export default function Header()  {
    return (
        <div>
            <Navbar bg="dark" variant={"dark"} expand="lg" style={{paddingTop: '2px', paddingBottom: '2px'}}>
                <img
                    src={logo}
                    width="55"
                    height="55"
                    className="d-inline-block align-top"
                    style={{marginLeft: '20px', marginRight: '20px'}}
                    alt=""
                />
                <Navbar.Toggle aria-controls="navbarScroll" />
                {/* <Navbar.Collapse id="navbarScroll" >
                    <Nav
                        className="mr-auto my-2 my-lg-0"
                        style={{ maxHeight: '100px', fontSize: '18px' }}
                        navbarScroll
                    >
                        <Nav.Link as={Link} to="/login" style={{marginLeft: '5px'}}>Login</Nav.Link>
                        <Nav.Link as={Link} to="/admin" style={{marginLeft: '15px'}}>Admin</Nav.Link>                        
                    </Nav>
                </Navbar.Collapse> */}
            </Navbar>
        </div>
    )
}

