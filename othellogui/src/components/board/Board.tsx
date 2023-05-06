import React from 'react';
import './board.css';
import { Square } from '../index';

const Board = () => {
  const renderSquares = () => {
    const squares = [];
    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        let squareId = `${row}-${col}`;
        squares.push(<Square key={squareId} state={0} />);
      }
    }
    return squares;
  };

  return (
    <div className="othello_play">
      <div className="othello_board">
        {renderSquares()}
      </div>
    </div>
  )
};

export default Board;
