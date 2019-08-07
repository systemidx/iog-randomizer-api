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
                            <FormRadio inline name="easy" checked={seedGeneratorStore.difficulty === "easy"} onChange={() => { this.changeDifficulty('easy')}}>Easy</FormRadio>
                            <FormRadio inline name="normal" checked={seedGeneratorStore.difficulty === "normal"} onChange={() => { this.changeDifficulty('normal')}}>Normal</FormRadio>
                            <FormRadio inline name="hard" checked={seedGeneratorStore.difficulty === "hard"} onChange={() => { this.changeDifficulty('hard')}}>Hard</FormRadio>
                            <FormRadio inline name="extreme" checked={seedGeneratorStore.difficulty === "extreme"} onChange={() => { this.changeDifficulty('extreme')}}>Extreme</FormRadio>
                        </CardBody>
                    </Card>                            
                </Container>
            )
        }
    }
)

export default SeedDifficulty