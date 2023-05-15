import React from 'react'
import './header.css'
// import headerImage from '../../assets/headerImage.png'

const Header: React.FC = (): JSX.Element => {
  const flaskHTML = '<i class="devicon-flask-original-wordmark"></i>'
  const pytorchHTML = '<i class="devicon-pytorch-plain-wordmark colored"></i>'
  const openaiHTML = '<i class="devicon-openal-plain colored"></i>'
  const reactHTML = '<i class="devicon-react-original-wordmark colored"></i>'
  const typescriptHTML = '<i class="devicon-typescript-plain colored"></i>'
  const pythonHTML = '<i class="devicon-python-plain-wordmark colored"></i>'

  return (
    <div className="othello_header_padding">
        <div className="othello_headline" id="explain">
          <h1> OthelloAI </h1>
        </div>
        <div className="othello_header_main_content">
          <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/devicons/devicon@v2.15.1/devicon.min.css"/>
          <div className="othello_header_main_content_image">
            <a href='https://react.dev'>
              <div dangerouslySetInnerHTML={{ __html: reactHTML }} style={{ fontSize: '2vw' }} />
            </a>
            <a href='https://www.typescriptlang.org'>
              <div dangerouslySetInnerHTML={{ __html: typescriptHTML }} style={{ fontSize: '2vw' }} />
            </a>
            <a href='https://www.python.org'>
              <div dangerouslySetInnerHTML={{ __html: pythonHTML }} style={{ fontSize: '2vw' }} />
            </a>
          </div>
          <div className="othello_header_main_content_text">
            <p>
              Welcome to OthelloAI! Here, you have the opportunity to challenge two types of artificial intelligence, putting your strategic abilities to the test against a machine. We offer two distinct AI implementations: one model that employs a combination of minimax algorithm, tuned heuristics, and alpha-beta pruning, and another model that utilizes PyTorch, reinforcement learning, neural networks, and OpenAI Gym.
              Playing against these two AI models can provide you with a unique opportunity to learn and improve your gameplay, discovering what ideas the AI prioritizes.
            </p>
          </div>
          <div className="othello_header_main_content_image">
            <a href='https://pytorch.org'>
              <div dangerouslySetInnerHTML={{ __html: pytorchHTML }} style={{ fontSize: '2vw' }} />
            </a>
            <a href='https://openai.com'>
              <div dangerouslySetInnerHTML={{ __html: openaiHTML }} style={{ fontSize: '2vw' }} />
            </a>
            <a href='https://flask.palletsprojects.com/en/2.3.x/'>
              <div dangerouslySetInnerHTML={{ __html: flaskHTML }} style={{ fontSize: '2vw', color: 'white' }} />
            </a>
          </div>
      </div>
    </div>
  )
}

export default Header
