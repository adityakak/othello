import React from 'react'
import './square.css'
import whitePiece from '../../assets/whitePiece.png'
import blackPiece from '../../assets/blackPiece.png'

interface SquareProps {
  key: string
  value: string
  state: number// 0 = empty, 1 = white, 2 = black, 1 white transparent, 3 black transparent
  onClick: () => void
}

const Square: React.FC<SquareProps> = props => {
  const handleClick = (): void => {
    props.onClick?.()
  }
  if (props.state === 0) {
    return <button className="othello_square" id={props.value} onClick={handleClick}>  </button>
  } else if (props.state === 1) {
    return <button className="othello_square" id={props.value}> <img src={whitePiece} alt="White" /> </button>
  } else if (props.state === 2) {
    return <button className="othello_square" id={props.value}> <div className="othello_black"> <img src={blackPiece} alt="Black" /> </div> </button>
  } else if (props.state === 3) {
    return <button className="othello_square" id={props.value} onClick={handleClick}> <div className="othello_white_trans"> <img src={whitePiece} alt="White Trans" /> </div> </button>
  } else {
    return <button className="othello_square" id={props.value} onClick={handleClick}> <div className="othello_black_trans"> <img src={blackPiece} alt="Black Trans" /> </div> </button>
  }
}

export default Square
