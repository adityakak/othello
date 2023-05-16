import React from 'react'

import './slider.css'

interface SliderProps {
  id: string
  onChange: (isChecked: boolean) => void
  'data-on'?: string
  isChecked: boolean
  'data-off'?: string
  description?: string
  canSlide: boolean
}

const Slider: React.FC<SliderProps> = props => {
  const onChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    if (props.canSlide) {
      // eslint-disable-next-line @typescript-eslint/strict-boolean-expressions, @typescript-eslint/prefer-optional-chain
      props.onChange && props.onChange(event.target.checked)
    }
  }

  const labelId = `label-${props.id}`
  const descriptionId = `description-${props.id}`

  const labelBy = labelId + ' ' + descriptionId
  return (
        <label htmlFor={props.id} className="switch">
            <input
                id={props.id}
                type="checkbox"
                role="switch"
                data-on={props['data-on']}
                checked={props.isChecked}
                data-off={props['data-off']}
                onChange={onChange}
                aria-checked={props.isChecked}
                aria-labelledby={labelBy}
            />
        </label>
  )
}

Slider.defaultProps = {
  'data-on': 'ON',
  'data-off': 'OFF'
}

export default Slider
