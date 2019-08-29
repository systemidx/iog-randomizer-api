import React, { Fragment } from 'react'
import { observer } from 'mobx-react'
import { FormInput, InputGroup, InputGroupAddon, InputGroupText } from 'shards-react'

import { Button, Tooltip, Grid } from '@material-ui/core'
import RedoIcon from '@material-ui/icons/Redo'

import seedGeneratorStore from '../../../stores/generator'
import detailsStore from '../../../stores/details'

const SeedForm = observer(
    class SeedForm extends React.Component {
        setSeed(seed) {
            if (isNaN(seed) || seed < 0) {
                seedGeneratorStore.setError('Hey, man. You need to enter a valid non-negative integer for a seed!')
                return
            }

            seedGeneratorStore.setSeed(seed)
        }

        render() {
            return (
                <Fragment>
                    <Grid container spacing={2} alignItems="center">
                        <Grid item>
                            <InputGroup>
                                <InputGroupAddon type="prepend">
                                    <InputGroupText>Seed</InputGroupText>
                                </InputGroupAddon>
                                <FormInput value={detailsStore.seed} onChange={(e) => this.setSeed(e.target.value)} type="text" />
                            </InputGroup>
                        </Grid>
                        <Grid item xs>
                            <Tooltip title="Randomize Seed">
                                <Button variant="contained" color="primary" onClick={detailsStore.randomizeSeed}><RedoIcon /></Button>
                            </Tooltip>
                        </Grid>
                    </Grid>
                </Fragment>
            )
        }
    }
)

export default SeedForm