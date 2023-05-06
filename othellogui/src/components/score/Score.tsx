import React from 'react'
import './score.css';
import whitePiece from '../../assets/whitePiece.png';
import blackPiece from '../../assets/blackPiece.png';

interface ScoreProps {
  whiteScore: number;
  blackScore: number;
}

const Score: React.FC<ScoreProps> = props => {
  return (
    <div className="othello_score">
      <div className="othello_score_box">
        <div className="othello_whiteScore">
          <img src={whitePiece} alt="whitePiece"/>
        </div>
        <span className="othello_score_text_white">{props.whiteScore}</span>
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
  blackScore: 2
}


export default Score