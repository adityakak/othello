import React, { useEffect, useState } from 'react'
import './board.css'
import { Square } from '../index'
import { Score } from '../../components'

interface BoardProps {
  engineMode: boolean // true = minimax, false = neural network
  engineSide: boolean // true = black, false = white
  gameMode: boolean // true = start, false = resign
}

interface BoardState {
  board: number[][]
  whiteScore: number
  blackScore: number
  turn: number // 0 no one, 1 white, 2 black
  row: number
  col: number
  move: number
}

const Board: React.FC<BoardProps> = props => {
  const humanSide = props.engineSide ? 'o' : 'x'
  const humanSideTurn = props.engineSide ? 2 : 1 // Number representing the color of the human player

  const aiSide = props.engineSide ? 'x' : 'o'
  const aiSideTurn = props.engineSide ? 1 : 2

  const initialArray: number[][] = Array.from({ length: 8 }, () => Array(8).fill(0))
  initialArray[3][3] = 1
  initialArray[3][4] = 2
  initialArray[4][3] = 2
  initialArray[4][4] = 1

  const initialBoardState: BoardState = {
    board: initialArray,
    whiteScore: 2,
    blackScore: 2,
    turn: 0,
    row: -1,
    col: -1,
    move: 0
  }

  const [boardState, setBoardState] = useState<BoardState>(initialBoardState)
  const [isClickable, setIsClickable] = useState<boolean>(true)

  useEffect(() => {
    if (props.engineSide) {
      if (!isClickable) return
      if (boardState.turn === 3) return
      setIsClickable(false)
      setBoardState(prevState => {
        const updatedBoard = [...prevState.board]
        updatedBoard[3][2] = 0
        updatedBoard[2][3] = 0
        updatedBoard[4][5] = 0
        updatedBoard[5][4] = 0
        return {
          ...prevState,
          board: updatedBoard,
          turn: 1
        }
      })
      setIsClickable(true)
    } else {
      if (!isClickable) return
      if (boardState.turn === 3) return
      setIsClickable(false)
      setBoardState(prevState => {
        const updatedBoard = [...prevState.board]
        updatedBoard[3][2] = 4
        updatedBoard[2][3] = 4
        updatedBoard[4][5] = 4
        updatedBoard[5][4] = 4
        return {
          ...prevState,
          board: updatedBoard
        }
      })
      setIsClickable(true)
    }
  }, [props.gameMode, props.engineSide])

  useEffect(() => {
    if (boardState.turn === humanSideTurn && boardState.row !== -1 && boardState.col !== -1 && props.gameMode) {
      fetch('http://127.0.0.1:5000/validSquares', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json'
        },
        body: JSON.stringify({ board: boardState.board, player: humanSide, coordinate: [boardState.row, boardState.col], move: boardState.move })
      })
        .then(async res => await res.json())
        .then(data => {
          setBoardState({
            board: data.board,
            // eslint-disable-next-line @typescript-eslint/strict-boolean-expressions
            turn: (data.valid) ? aiSideTurn : humanSideTurn,
            row: -1,
            col: -1,
            whiteScore: data.whiteScore,
            blackScore: data.blackScore,
            move: data.move
          })
        })
        .catch(err => { console.log(err) })
    }
    if (boardState.turn === aiSideTurn && props.gameMode) {
      fetch('http://127.0.0.1:5000/minimax', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json'
        },
        body: JSON.stringify({ board: boardState.board, player: aiSide, move: boardState.move })
      })
        .then(async res => await res.json())
        .then(data => {
          setBoardState(prevState => ({
            ...prevState,
            turn: data.gameOver === 1 ? aiSideTurn : (data.gameOver === 0 ? humanSideTurn : 3), // 0 Normal , 1 Keep, 2 Game Over
            board: data.board,
            whiteScore: data.whiteScore,
            blackScore: data.blackScore,
            move: data.move
          }))
        })
        .catch(err => { console.log(err) })
    }
  }, [boardState])

  const handleSquareClick = (row: number, col: number): void => {
    if (!isClickable) return
    if (boardState.turn === 3) return
    if (!props.gameMode) return
    setIsClickable(false)
    setBoardState(prevState => ({
      ...prevState,
      turn: props.engineSide ? 2 : 1,
      row,
      col
    }))
    setIsClickable(true)
  }

  const renderSquares = (): JSX.Element[] => {
    const squares = []
    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        const squareId = `${row}-${col}`
        squares.push(<Square key={squareId} value={squareId} state={boardState.board[row][col]} onClick={() => {
          handleSquareClick(row, col)
        }} />)
      }
    }
    return squares
  }

  return (
    <div className="othello_play">
      {boardState.turn !== 3
        ? (
        <Score
          whiteScore={boardState.whiteScore}
          blackScore={boardState.blackScore}
          arrowSide={boardState.move % 2 === 0}
        />
          )
        : (
        <div className="othello_gameover_wrapper">
          <div className="othello_gameover">
            <h1>Game Over</h1>
            <h2>{boardState.whiteScore > boardState.blackScore ? 'White Wins' : 'Black Wins'}</h2>
            <h3> Score: {boardState.whiteScore} - {boardState.blackScore} </h3>
          </div>
        </div>
          )
      }
      <div className="othello_board">
        {renderSquares()}
      </div>
    </div>
  )
}

export default Board
