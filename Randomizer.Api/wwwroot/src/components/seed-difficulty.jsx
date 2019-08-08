import React from 'react'
import { observer } from 'mobx-react'
import { Card, CardBody, CardTitle, Container, FormRadio } from 'shards-react'

import seedGeneratorStore from '../stores/generator'

const SeedDifficulty = observer(
    class SeedDifficulty extends React.Component {
        constructor(props) {
            super(props)

            this.changeDifficulty = this.changeDifficulty.bind(this)
        }

        changeDifficulty(difficulty) {
            seedGeneratorStore.setDifficulty(difficulty)
        }

        render() {
            return (
                <Container>
                    <Card>                    
                        <CardBody>
                            <CardTitle>Difficulty</CardTitle>
                            <FormRadio inline name="Easy" checked={seedGeneratorStore.difficulty === "Easy"} onChange={() => { this.changeDifficulty('Easy')}}>Easy</FormRadio>
                            <FormRadio inline name="Normal" checked={seedGeneratorStore.difficulty === "Normal"} onChange={() => { this.changeDifficulty('Normal')}}>Normal</FormRadio>
                            <FormRadio inline name="Hard" checked={seedGeneratorStore.difficulty === "Hard"} onChange={() => { this.changeDifficulty('Hard')}}>Hard</FormRadio>
                            <FormRadio inline name="Extreme" checked={seedGeneratorStore.difficulty === "Extreme"} onChange={() => { this.changeDifficulty('Extreme')}}>Extreme</FormRadio>
                        </CardBody>
                    </Card>                            
                </Container>
            )
        }
    }
)

export default SeedDifficulty