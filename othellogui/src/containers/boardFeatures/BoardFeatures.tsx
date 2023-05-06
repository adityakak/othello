import React, { useState } from 'react'
import './boardFeatures.css';
import { Score, Slider, Board } from '../../components';

const BoardFeatures = () => {
  const [sliderMode, setSliderMode] = useState(false);

  const handleSliderChange = (isChecked: boolean) => {
    setSliderMode(isChecked);
  };

  return (
    <div className="othello_play" id="play">
      <h1> Play Against AI </h1>
      <div className="othello_slider_div">
        <Slider
          id="mySlider"
          onChange={handleSliderChange}
          isChecked={sliderMode}
          data-on="MM"
          data-off="NN"
        />
      </div>
      <div className="othello_slider_div_caption">
        <p> Choose between playing against a minimax algorithim (MM) or a neural network (NN) version of the AI</p>
      </div>
      <Board engineMode={sliderMode} />
    </div>
  )
}

export default BoardFeatures

