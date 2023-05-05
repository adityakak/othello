import React from 'react'
import './information.css';

const Information = () => {
  return (
    <div className="othello_information" id="learn">
      <h1> How To Play </h1>
      <h2> Rules of The Game</h2>
      <div className="othello_rules">
        <div>
          <p> 1. The game is played on an 8x8 board with 64 identical game pieces called disks, which are light on one side and dark on the other.</p>
        </div>
        <div>
          <p> 2. The game begins with four disks already placed on the board: two light disks and two dark disks, arranged with dark disks at D4 and E5 and light disks at D5 and E4.</p>
        </div>
      </div>
    </div>
  )
}

export default Information

