import React from 'react'
import './information.css';
import othelloStart from '../../assets/othelloStart.png';
import othelloPossible from '../../assets/othelloPossible.png';

const Information = () => {
  return (
    <div className="othello_information" id="learn">
      <h1> How To Play </h1>
      <h2> Rules of The Game</h2>
      <div className="othello_rules">
        <div>
          <p> 1. The game is played on an 8x8 board with 64 identical game pieces called disks, which are light on one side and dark on the other. (Columns are indexed A-H from left to right and rows are indexed 0-8 bottom to top)</p>
        </div>
        <div>
          <p> 2. The game begins with four disks already placed on the board: two light disks and two dark disks, arranged with dark disks at D4 and E5 and light disks at D5 and E4. The dark player moves first.</p>
        </div>
        <img src={othelloStart} alt="othelloStart"/>
        <div>
          <p> 3. Dark must place a dark disk on the board, in such a position that there exists at least one straight (horizontal, vertical, or diagonal) occupied line between the new disk and another dark disk, with one or more contiguous light disks between them. In the below situation, dark has the following options for moves: </p>
        </div>
        <img src={othelloPossible} alt="othelloPossible"/>
        <div>
          <p> 4. If a player has no possible moves, they must pass their turn, giving the opponent another one. If both players have no possible moves, or if the board is full of disks then the game is over</p>
        </div>
      </div>
    </div>
  )
}

export default Information

