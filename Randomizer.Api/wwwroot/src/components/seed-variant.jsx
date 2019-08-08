import React from 'react'
import { observer } from 'mobx-react'
import { Card, CardBody, CardTitle, Container, FormRadio, FormGroup } from 'shards-react'

import seedGeneratorStore from '../stores/generator'

const SeedVariant = observer(
    class SeedVariant extends React.Component {
        constructor(props) {
            super(props)

            this.setVariant = this.setVariant.bind(this)
            this.setMode = this.setMode.bind(this)
            this.setFirebird = this.toggleFirebird.bind(this)
        }

        setVariant(variant) {
            seedGeneratorStore.setVariant(variant)
        }

        setMode(mode) {
            seedGeneratorStore.setMode(mode)
        }

        toggleFirebird() {
            seedGeneratorStore.setFirebird(!seedGeneratorStore.firebird)
        }

        render() {
            return (
                <Container style={{marginTop: 20}}>
                    <Card>                    
                        <CardBody>
                            <CardTitle>Variations</CardTitle>
                            <FormGroup>
                                <FormRadio inline name="None" checked={seedGeneratorStore.variant === "None"} onChange={() => { this.setVariant('None')}}>None</FormRadio>
                                <FormRadio inline name="OHKO" checked={seedGeneratorStore.variant === "OHKO"} onChange={() => { this.setVariant('OHKO')}}>One Hit KO</FormRadio>
                            </FormGroup>
                            <FormGroup>
                                <FormRadio inline name="Completable" checked={seedGeneratorStore.mode === "Completable"} onChange={() => { this.setMode('Completable')}}>Completable</FormRadio>
                                <FormRadio inline name="Beatable" checked={seedGeneratorStore.mode === "Beatable"} onChange={() => { this.setMode('Beatable')}}>Beatable</FormRadio>
                                <FormRadio inline name="Chaos" checked={seedGeneratorStore.mode === "Chaos"} onChange={() => { this.setMode('Chaos')}}>Chaos</FormRadio>
                            </FormGroup>
                            {/* <FormCheckbox checked={seedGeneratorStore.firebird === true} onChange={() => { this.toggleFirebird()}}>Firebird</FormCheckbox>                             */}
                        </CardBody>
                    </Card>                            
                </Container>
            )
        }
    }
)

export default SeedVariant