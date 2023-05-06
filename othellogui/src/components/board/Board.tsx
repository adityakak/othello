import React, { useState } from 'react';
import './board.css';
import { Square } from '../index';

const Board = () => {
  const initialArray: number[][] = Array.from({ length: 8 }, () => Array(8).fill(0));
  initialArray[3][3] = 1;
  initialArray[3][4] = 2;
  initialArray[4][3] = 2;
  initialArray[4][4] = 1;

  const [boardState, setBoardState] = useState<number[][]>(initialArray);
  const [isClickable, setIsClickable] = useState<boolean>(true);

  const handleSquareClick = (row: number, col: number) => {
    if (!isClickable) return; 
    const updatedBoardState = boardState.map((rowArr, rowIndex) =>
      rowIndex === row ? rowArr.map((value, colIndex) => (colIndex === col ? 2 : value)) : rowArr
    );
    setBoardState(updatedBoardState);
    setIsClickable(false); 
    setTimeout(() => {
      setIsClickable(true);
    }, 3000);
  };

  const renderSquares = () => {
    const squares = [];
    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        let squareId = `${row}-${col}`;
        squares.push(<Square key={squareId} value={squareId} state={boardState[row][col]} onClick={() => handleSquareClick(row, col)} />);
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
