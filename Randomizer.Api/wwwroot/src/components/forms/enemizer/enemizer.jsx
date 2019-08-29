import React from 'react'
import { observer } from 'mobx-react'
import { InputGroup, InputGroupAddon, InputGroupText, FormSelect } from 'shards-react'

import enemizerStore from '../../../stores/enemizer'

const EnemizerForm = observer(
    class EnemizerForm extends React.Component {
        render() {
            return (
                <InputGroup>
                    <InputGroupAddon type="prepend">
                        <InputGroupText>Enemizer</InputGroupText>
                    </InputGroupAddon>
                    <FormSelect defaultValue={enemizerStore.enemizer} onChange={(v) => enemizerStore.setEnemizer(v.target.value)}>
                        <option value="None">None</option>
                        <option value="Limited">Limited</option>
                        <option value="Balanced">Balanced</option>
                        <option value="Full">Full</option>
                        <option value="Insane">Insane</option>
                    </FormSelect>
                </InputGroup>
            )
        }
    }
)

export default EnemizerForm