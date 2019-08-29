import React from 'react'
import { observer } from 'mobx-react'
import { InputGroup, InputGroupAddon, InputGroupText, FormSelect } from 'shards-react'

import detailsStore from '../../../stores/details'

const DifficultyForm = observer(
    class DifficultyForm extends React.Component {
        render() {
            return (
                <InputGroup>
                    <InputGroupAddon type="prepend">
                        <InputGroupText>Difficulty</InputGroupText>
                    </InputGroupAddon>
                    <FormSelect defaultValue={detailsStore.difficulty} onChange={(v) => detailsStore.setDifficulty(v)}>
                        <option value="Easy">Easy</option>
                        <option value="Normal">Normal</option>
                        <option value="Hard">Hard</option>
                        <option value="Extreme">Extreme</option>
                    </FormSelect>
                </InputGroup>
            )
        }
    }
)

export default DifficultyForm