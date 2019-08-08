import React from 'react'
import { observer } from 'mobx-react'
import { Card, CardBody, CardTitle, Container, FormGroup, FormRadio, FormSelect } from 'shards-react'

import seedGeneratorStore from '../stores/generator'

const SeedGoal = observer(
    class SeedGoal extends React.Component {

        setGoal(difficulty) {
            seedGeneratorStore.setGoal(difficulty)
        }

        setStatues(statues) {
            seedGeneratorStore.setStatues(statues.target.value)
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
                            </FormGroup>
                            { seedGeneratorStore.goal === 'Dark Gaia' && (
                                <FormGroup>
                                    <label>
                                        Statues:
                                    <FormSelect defaultValue={seedGeneratorStore.statues} onChange={(v) => this.setStatues(v)}>
                                        <option value="0">0</option>
                                        <option value="1">1</option>
                                        <option value="2">2</option>
                                        <option value="3">3</option>
                                        <option value="4">4</option>
                                        <option value="5">5</option>
                                        <option value="6">6</option>
                                        <option value="Random">Random</option>
                                    </FormSelect>
                                    </label>
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