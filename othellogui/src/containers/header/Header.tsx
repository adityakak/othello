import React from 'react'
import './header.css'
import headerImage from '../../assets/headerImage.png'

const Header: React.FC = (): JSX.Element => {
  return (
    <div className="othello_header_padding">
        <div className="othello_headline" id="explain">
          <h1> OthelloAI </h1>
        </div>
        <div className="othello_header_main_content">
          <img src={headerImage} alt="aiImage"/>
          <p> Welcome to OthelloAI! Here, you have the opportunity to challenge two types of artificial intelligence, putting your strategic abilities to the test against a machine. We offer two distinct AI implementations: one model that employs a combination of minimax algorithm, tuned heuristics, and alpha-beta pruning, and another model that utilizes PyTorch, reinforcement learning, neural networks, and OpenAI Gym.
              Playing against these two AI models can provide you with a unique opportunity to learn and improve your gameplay, discovering what ideas the AI prioritizes.
          </p>
      </div>
    </div>
  )
}

export default Header
