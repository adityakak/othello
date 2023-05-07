import React, { useEffect, useState } from 'react';
import './board.css';
import { Square } from '../index';
import { Score } from '../../components';

interface BoardProps {
  engineMode: boolean; // true = minimax, false = neural network
}

interface BoardState {
  board: number[][];
  whiteScore: number;
  blackScore: number;
  turn: number; //0 no one, 1 white, 2 black
  row: number;
  col: number;
}

const Board: React.FC<BoardProps> = props => {
  const initialArray: number[][] = Array.from({ length: 8 }, () => Array(8).fill(0));
  initialArray[3][3] = 1;
  initialArray[3][4] = 2;
  initialArray[4][3] = 2;
  initialArray[4][4] = 1;

  const initialBoardState: BoardState = {
    board: initialArray,
    whiteScore: 2,
    blackScore: 2,
    turn: 0,
    row: -1,
    col: -1,
  };

  const [boardState, setBoardState] = useState<BoardState>(initialBoardState);
  const [isClickable, setIsClickable] = useState<boolean>(true);

  useEffect(() => { 
    if(boardState.turn == 1 && boardState.row != -1 && boardState.col != -1) {
      fetch('http://127.0.0.1:5000/validSquares', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify({ board: boardState.board, player: 'x', coordinate: [boardState.row, boardState.col] }),
    })
      .then(res => res.json())
      .then(data => {
        console.log(data, "1");
        setBoardState({
          board: data.board,
          turn: data.valid ? 2 : 1,
          row: -1,
          col: -1,
          whiteScore: data.whiteScore,
          blackScore: data.blackScore,
        });
      });
    }
    if(boardState.turn == 2) {
      console.log(boardState, "2");
      fetch('http://127.0.0.1:5000/minimax', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify({ board: boardState.board, player: 'o'}),
      })
        .then(res => res.json())
        .then(data => {
          setBoardState(prevState => ({
            ...prevState,
            turn: data.gameOver === 1 ? 2 : (data.gameOver === 0 ? 1 : 3),  //0 Normal , 1 Keep, 2 Game Over
            board: data.board,
            whiteScore: data.whiteScore,
            blackScore: data.blackScore,
          }));
        });
    }

  }, [boardState]);

  const handleSquareClick = (row: number, col: number) => {  //AI plays white, human plays black
    if (!isClickable) return;
    if (boardState.turn == 3) return;
    setIsClickable(false);
    setBoardState(prevState => ({
      ...prevState,
      turn: 1,
      row: row,
      col: col, 
    }));
    /*
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
    */
    setIsClickable(true);
  };

  const renderSquares = () => {
    const squares = [];
    console.log(boardState, "render");
    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        let squareId = `${row}-${col}`;
        squares.push(<Square key={squareId} value={squareId} state={boardState.board[row][col]} onClick={() => handleSquareClick(row, col)} />);
      }
    }
    return squares;
  };

  return (
    <div className="othello_play">
      <Score
        whiteScore={boardState.whiteScore}
        blackScore={boardState.blackScore}
      />
      <div className="othello_board">
        {renderSquares()}
      </div>
    </div>
  )
};

export default Board;
