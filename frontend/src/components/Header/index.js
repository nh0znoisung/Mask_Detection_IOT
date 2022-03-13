import React from 'react'
import { Navbar } from 'react-bootstrap'
import logo from './logo.png';
import logoutimg from './logout.png';
import {useNavigate} from 'react-router-dom'
import { useAuth } from "../../contexts/AuthContext"


export default function Header()  {
    const navigate = useNavigate();
    const { logout } = useAuth()
    async function handleLogout() {
        await logout()
        navigate('/login');
        //   catch {
        //     setError("Failed to log out")
        //   }
    }
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
                <Navbar.Toggle aria-controls="navbarScroll"  />
                <Navbar.Collapse id="navbarScroll"  className="justify-content-end" onClick={handleLogout}>
                    {/* <Nav
                        className="mr-auto my-2 my-lg-0"
                        style={{ maxHeight: '100px', fontSize: '18px' }}
                        navbarScroll
                    >
                        <Nav.Link as={Link} to="/login" style={{marginLeft: '5px'}}>Login</Nav.Link>
                        <Nav.Link as={Link} to="/admin" style={{marginLeft: '15px'}}>Admin</Nav.Link>                        
                    </Nav> */}
                    <img
                        src={logoutimg}
                        width="40"
                        height="40"
                        className="d-inline-block align-top"
                        style={{ marginRight: '30px', cursor: 'pointer' }}
                        alt=""
                        
                    />
                </Navbar.Collapse>
            </Navbar>
        </div>
    )
}

