import React from 'react'
import { observer } from 'mobx-react'
import { FormSelect, InputGroup, InputGroupAddon, InputGroupText } from 'shards-react'

import variantsStore from '../../../stores/variants'

const StartLocationForm = observer(
    class StartLocationForm extends React.Component {
        render() {
            return (
                <InputGroup>
                    <InputGroupAddon type="prepend">
                        <InputGroupText>Starting Location</InputGroupText>
                    </InputGroupAddon>
                    <FormSelect defaultValue={variantsStore.startLocation} onChange={(v) => variantsStore.setStartLocation(v.target.value)}>
                        <option value="South Cape">South Cape</option>
                        <option value="Safe">Safe</option>
                        <option value="Unsafe">Unsafe</option>
                        <option value="Forced Unsafe">Forced Unsafe</option>
                    </FormSelect>
                </InputGroup>
            )
        }
    }
)

export default StartLocationForm