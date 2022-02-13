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
            The Team
          </NavLink> 
          <NavLink to="/Project" activeStyle>
            Our Project
          </NavLink>
          <NavLink to="/Diagrams" activeStyle>
            Diagrams
          </NavLink>
          <NavLink to="/Documents" activeStyle>
            Slides/Videos
          </NavLink>

        </NavMenu>
      </Nav>
    </>
  );
};
  
export default Navbar;