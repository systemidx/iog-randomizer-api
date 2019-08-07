import React from 'react'
import { Navbar, NavbarBrand } from 'shards-react'

export default class Navigation extends React.Component {
    render() {
        return (
            <Navbar type="dark" theme="primary">
                <NavbarBrand href="#">Illusion of Gaia Randomizer</NavbarBrand>
            </Navbar>
        )
    }
}