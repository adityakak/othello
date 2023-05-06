import React from 'react';
import './square.css';
import whitePiece from '../../assets/whitePiece.png';
import blackPiece from '../../assets/blackPiece.png';

interface SquareProps {
    key: string;
    state: number; // 0 = empty, 1 = white, 2 = black
  }

const Square: React.FC<SquareProps> = props => {
    if(props.state === 0) {
        return <button className="othello_square" id={props.key}>  </button>;
    } else if(props.state === 1) {
        return <button className="othello_square" id={props.key}> <img src={whitePiece} alt="White" /> </button>;
    }
    else{
        return <button className="othello_square" id={props.key}> <div className="othello_black"> <img src={blackPiece} alt="Black" /> </div> </button>;
    }
};

export default Square;
