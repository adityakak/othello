import React, { useEffect, useState } from 'react'
import './score.css'
import whitePiece from '../../assets/whitePiece.png'
import blackPiece from '../../assets/blackPiece.png'

interface ScoreProps {
  whiteScore: number
  blackScore: number
  arrowSide: boolean
}

type Classes = Record<number, string>

const Score: React.FC<ScoreProps> = props => {
  const [direction, setDirection] = useState(0)
  const [arrowClass, setArrowClass] = useState('arrow-right')
  const classes: Classes = {
    0: 'arrow right',
    1: 'arrow down',
    2: 'arrow left',
    3: 'arrow up'
  }

  useEffect(() => {
    setDirection(0)
  }, [])
  useEffect(() => {
    setArrowClass(classes[direction])
  }, [direction])
  useEffect(() => {
    setDirection(props.arrowSide ? 0 : 2)
  }, [props.arrowSide])

  return (
    <div className="othello_score">
      <div className="othello_score_box">
        <div className="othello_whiteScore">
          <img src={whitePiece} alt="whitePiece"/>
        </div>
        <span className="othello_score_text_white">{props.whiteScore}</span>
        <div className="othello_score_arrow">
          <p><i className={arrowClass}></i></p>
        </div>
        <span className="othello_score_text_black">{props.blackScore}</span>
        <div className="othello_blackScore">
          <img src={blackPiece} alt="blackPiece"/>
        </div>
      </div>
    </div>
  )
}

Score.defaultProps = {
  whiteScore: 2,
  blackScore: 2,
  arrowSide: false
}

export default Score
