import React from 'react'
import './header.css';
import headerImage from '../../assets/headerImage.png';

const Header = () => {
  return (
    <div className="othello_header_padding">
      <div className="othello_header"> 
        <div className="othello_headline" id="explain">
          <h1> OthelloAI </h1>
        </div>
        <div className="othello_header_main_content">
          <img src={headerImage} alt="aiImage"/>
          <p> Welcome to our website, where you can play against two types of artificial intelligence! We offer you the chance to test your strategic skills against two different types of AI. One of our AI models uses the minimax algorithm with alpha beta pruning, which is a popular and powerful technique for game playing. The other AI model utilizes an implementation of PyTorch, which is a popular machine learning framework.
              Playing against these two AI models can provide you with a unique opportunity to learn and improve your gameplay. You can choose to play against either of these models or even against both of them in a single game. Our website is designed to provide you with a seamless and immersive experience, and we are confident that you will enjoy the challenge of playing against our AI models.
              So, what are you waiting for? Come and try your skills against our AI models today! 
          </p>
        </div>
      </div>
    </div>
  )
}

export default Header

