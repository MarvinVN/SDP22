import React from 'react';
import { Nav, NavLink, NavMenu } from "./NavbarElements";
  
const Navbar = () => {
  return (
    <>
      <Nav style={{position:'sticky', top:'0'}}>
        <NavMenu>
          <NavLink to="/" activeStyle>
            Home
          </NavLink>
          <NavLink to="/TeamPage" activeStyle>
            Our Team
          </NavLink>
        </NavMenu>
      </Nav>
    </>
  );
};
  
export default Navbar;