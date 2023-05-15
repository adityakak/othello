import React, { useState } from 'react'
import './boardFeatures.css'
import { Slider, Board } from '../../components'
import Button from '@mui/material/Button'

const BoardFeatures = (): JSX.Element => {
  const [sliderModeAI, setSliderModeAI] = useState(false)
  const [sliderModeColor, setSliderModeColor] = useState(false)
  const [startMode, setStartMode] = useState(false)

  const handleSliderChangeAI = (isChecked: boolean): void => {
    setSliderModeAI(isChecked)
  }
  const handleSliderChangeColor = (isChecked: boolean): void => {
    setSliderModeColor(isChecked)
  }

  return (
    <div className="othello_play" id="play">
      <h1> Play Against AI </h1>
      <div className="othello_slider_div">
        <Slider
          id="aiSlider"
          onChange={handleSliderChangeAI}
          isChecked={sliderModeAI}
          data-on="MM"
          data-off="NN"
        />
        <Slider
          id="colorSlider"
          onChange={handleSliderChangeColor}
          isChecked={sliderModeColor}
          data-on="B"
          data-off="W"
        />
      </div>
      <div className='othello_button_div'>
        <Button variant="contained" onClick={() => { setStartMode(!startMode) }}> Start </Button>
      </div>
      {/* <div className="othello_slider_div_caption">
        <p> Choose between playing against a minimax algorithim (MM) or a neural network (NN) version of the AI</p>
      </div> */}
      <Board engineMode={sliderModeAI} />
    </div>
  )
}

export default BoardFeatures
