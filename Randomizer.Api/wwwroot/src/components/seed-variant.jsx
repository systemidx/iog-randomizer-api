import React from 'react'
import { observer } from 'mobx-react'
import { Card, CardBody, CardTitle, Container, FormRadio, FormCheckbox } from 'shards-react'

import seedGeneratorStore from '../stores/generator'

const SeedVariant = observer(
    class SeedVariant extends React.Component {
        constructor(props) {
            super(props)

            this.setVariant = this.setVariant.bind(this)
            this.setFirebird = this.toggleFirebird.bind(this)
        }

        setVariant(variant) {
            seedGeneratorStore.setVariant(variant)
        }

        toggleFirebird(firebird) {
            seedGeneratorStore.setFirebird(!seedGeneratorStore.firebird)
        }

        render() {
            return (
                <Container style={{marginTop: 20}}>
                    <Card>                    
                        <CardBody>
                            <CardTitle>Variations</CardTitle>
                            <FormRadio inline name="None" checked={seedGeneratorStore.variant === "None"} onChange={() => { this.setVariant('None')}}>None</FormRadio>
                            <FormRadio inline name="OHKO" checked={seedGeneratorStore.variant === "OHKO"} onChange={() => { this.setVariant('OHKO')}}>One Hit KO</FormRadio>
                            <FormCheckbox checked={seedGeneratorStore.firebird === true} onChange={() => { this.toggleFirebird()}}>Firebird</FormCheckbox>                            
                        </CardBody>
                    </Card>                            
                </Container>
            )
        }
    }
)

export default SeedVariant