import React, { useEffect, useState } from 'react';
import './board.css';
import { Square } from '../index';
import { Score } from '../../components';

interface BoardProps {
  engineMode: boolean; // true = minimax, false = neural network
}

const Board: React.FC<BoardProps> = props => {
  const initialArray: number[][] = Array.from({ length: 8 }, () => Array(8).fill(0));
  initialArray[3][3] = 1;
  initialArray[3][4] = 2;
  initialArray[4][3] = 2;
  initialArray[4][4] = 1;

  const [boardState, setBoardState] = useState<number[][]>(initialArray);
  const [isClickable, setIsClickable] = useState<boolean>(true);
  const [scoresData, setScoresData] = useState({
    whiteScore: 2,
    blackScore: 2,
  });
  const [possibleMovesData, setPossibleMovesData] = useState<boolean>(true);

  const handleSquareClick = (row: number, col: number) => {
    if (!isClickable) return;
    console.log(props.engineMode);
    setIsClickable(false);

    fetch('http://127.0.0.1:5000/validSquares', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify({ board: boardState, player: 'x', coordinate: [row, col] }),
    })
      .then(res => res.json())
      .then(data => {
        setPossibleMovesData(data.valid);
        setBoardState(data.board);
        setScoresData({ whiteScore: data.whiteScore, blackScore: data.blackScore });
        console.log(boardState);
      });

    if (possibleMovesData) {
      fetch('http://127.0.0.1:5000/minimax', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify({ board: boardState, player: 'o'}),
      })
        .then(res => res.json())
        .then(data => {
          setBoardState(data.board);
          setScoresData({ whiteScore: data.whiteScore, blackScore: data.blackScore });
        });
    }
    setIsClickable(true);
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
      <Score
        whiteScore={scoresData.whiteScore}
        blackScore={scoresData.blackScore}
      />
      <div className="othello_board">
        {renderSquares()}
      </div>
    </div>
  )
};

export default Board;
