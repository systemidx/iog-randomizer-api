import React from 'react'
import { Navbar, NavbarBrand, Nav, NavItem, NavLink } from 'shards-react'
import { FaGithub } from 'react-icons/fa'

export default class Navigation extends React.Component {
    render() {
        return (
            <Navbar type="dark" theme="primary">
                <NavbarBrand href="#"><span style={{ fontWeight: 'bold'}}>Illusion of Gaia Randomizer</span><span style={{ marginLeft: 20}}>v1.5.1</span></NavbarBrand>
                <Nav navbar>
                    <NavItem><NavLink href="https://www.github.com/dontbagume/iogr"><FaGithub color="white" size="30" /></NavLink></NavItem>
                </Nav>
            </Navbar>
        )
    }
}