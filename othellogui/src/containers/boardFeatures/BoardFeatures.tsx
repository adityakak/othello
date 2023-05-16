import React, { useState } from 'react'
import './boardFeatures.css'
import { Slider, Board } from '../../components'
import Button from '@mui/material/Button'

const BoardFeatures = (): JSX.Element => {
  const [sliderModeAI, setSliderModeAI] = useState(false)
  const [sliderModeColor, setSliderModeColor] = useState(false)
  const [startMode, setStartMode] = useState(false)
  const [boardRenderKey, setBoardRenderKey] = useState(0)

  const handleSliderChangeAI = (isChecked: boolean): void => {
    setSliderModeAI(isChecked)
  }
  const handleSliderChangeColor = (isChecked: boolean): void => {
    setSliderModeColor(isChecked)
  }
  const handleResign: () => void = () => {
    setBoardRenderKey(prevKey => prevKey + 1)
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
      {!startMode
        ? (
      <div className='othello_button_div'>
        <Button variant="contained" onClick={() => { setStartMode(!startMode) }}> Start </Button>
      </div>
          )
        : (
      <div className='othello_button_div'>
        <Button variant="contained" onClick={() => { setStartMode(!startMode); handleResign() }}> Resign & Reset </Button>
      </div>
          )}
      <Board key={boardRenderKey} engineMode={sliderModeAI} engineSide={sliderModeColor} gameMode={startMode} />
    </div>
  )
}

export default BoardFeatures
