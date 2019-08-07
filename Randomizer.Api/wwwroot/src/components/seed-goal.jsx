import React from 'react'
import { observer } from 'mobx-react'
import { Card, CardBody, CardTitle, Container,FormCheckbox, FormInput, FormGroup, FormRadio } from 'shards-react'

import seedGeneratorStore from '../stores/generator'

const SeedGoal = observer(
    class SeedGoal extends React.Component {
        constructor(props) {
            super(props)

            this.setStatuesRandom = this.setStatuesRandom.bind(this)
        }

        setGoal(difficulty) {
            seedGeneratorStore.setGoal(difficulty)
        }

        setStatuesRandom() {
            seedGeneratorStore.toggleStatuesRandom()
        }

        render() {
            return (
                <Container style={{marginTop: 20}}>
                    <Card>                    
                        <CardBody>
                            <CardTitle>Goal</CardTitle>
                            <FormGroup>
                                <FormRadio inline name="Dark Gaia" checked={seedGeneratorStore.goal === "Dark Gaia"} onChange={() => { this.setGoal('Dark Gaia')}}>Dark Gaia</FormRadio>
                                <FormRadio inline name="Red Jewel Hunt" checked={seedGeneratorStore.goal === "Red Jewel Hunt"} onChange={() => { this.setGoal('Red Jewel Hunt')}}>Red Jewel Hunt</FormRadio>
                                <FormRadio inline name="Random" checked={seedGeneratorStore.goal === "Random"} onChange={() => { this.setGoal('Random')}}>Random</FormRadio>
                            </FormGroup>
                            { seedGeneratorStore.goal === 'Dark Gaia' && (
                                <FormGroup style={{ display: 'flex', flexDirection: 'row', alignContent: 'center', alignItems: 'center', justifyContent: 'space-between'}}>
                                    <label>Number of Statues (0 - 6): <FormInput disabled={seedGeneratorStore.statuesRandom} defaultValue={seedGeneratorStore.statues} onChange={ (v) => seedGeneratorStore.setStatues(v.target.value) } /></label>
                                    <FormCheckbox inline checked={seedGeneratorStore.statuesRandom === true} onChange={this.setStatuesRandom}>Random</FormCheckbox>
                                </FormGroup>
                            )}                            
                        </CardBody>
                    </Card>                            
                </Container>
            )
        }
    }
)

export default SeedGoal