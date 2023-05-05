import React from 'react'
import './navbar.css';
import { RiMenu3Line, RiCloseLine } from 'react-icons/ri';
import logo from '../../assets/logo.png';

const Navbar = () => {
  return (
    <div className="othello_navbar">
      <div className="othello_navbar_links">
        <div className='othello_navbar_logo'>
          <img src={logo} alt="logo"/>
        </div>
        <div className="othello_navbar_links_container">
          <p><a href="#explain">Description</a></p>
          <p><a href="#learn">How To Play</a></p>
          <p><a href="#play">Play</a></p>
        </div>
      </div>
    </div>
  )
}

export default Navbar