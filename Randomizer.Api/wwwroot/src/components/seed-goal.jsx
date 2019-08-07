import React from 'react'
import { observer } from 'mobx-react'
import { Card, CardBody, CardTitle, Container, FormRadio } from 'shards-react'

import seedGeneratorStore from '../stores/generator'

const SeedGoal = observer(
    class SeedGoal extends React.Component {
        constructor(props) {
            super(props)

            this.setGoal = this.setGoal.bind(this)
        }

        setGoal(difficulty) {
            seedGeneratorStore.setGoal(difficulty)
        }

        render() {
            return (
                <Container style={{marginTop: 20}}>
                    <Card>                    
                        <CardBody>
                            <CardTitle>Goal</CardTitle>
                            <FormRadio inline name="Dark Gaia" checked={seedGeneratorStore.goal === "Dark Gaia"} onChange={() => { this.setGoal('Dark Gaia')}}>Dark Gaia</FormRadio>
                            <FormRadio inline name="Red Jewel Hunt" checked={seedGeneratorStore.goal === "Red Jewel Hunt"} onChange={() => { this.setGoal('Red Jewel Hunt')}}>Red Jewel Hunt</FormRadio>
                            <FormRadio inline name="Random" checked={seedGeneratorStore.goal === "Random"} onChange={() => { this.setGoal('Random')}}>Random</FormRadio>
                        </CardBody>
                    </Card>                            
                </Container>
            )
        }
    }
)

export default SeedGoal