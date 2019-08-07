import React from 'react'
import { Button, Card, CardBody, CardTitle, Container, Form, FormInput, FormGroup, Row } from "shards-react";

import seedGeneratorStore from '../stores/generator'
import { observer } from 'mobx-react';

const SeedGenerator = observer(class SeedGenerator extends React.Component {
    state = {
        showDownload: false,
        romUri: null,
        romName: null,
        spoilerUri: null,
        spoilerName: null
    }

    constructor(props) {
        super(props)

        this.handleSubmit = this.handleSubmit.bind(this)
        this.handleDownloadRom = this.handleDownloadRom.bind(this)
        this.handleDownloadSpoiler = this.handleDownloadSpoiler.bind(this)
        this.handleRandomizeSeed = this.handleRandomizeSeed.bind(this)
        
        this.generateSeed = this.generateSeed.bind(this)
        this.requestSeed = this.requestSeed.bind(this)
        this.requestSpoiler = this.requestSpoiler.bind(this)

        this.fileInput = React.createRef();
        this.seedInput = React.createRef();
    }

    async generateSeed(fileToUpload) {
        seedGeneratorStore.setProcessing()

        try {
            await this.requestSeed(fileToUpload)
            await this.requestSpoiler()
    
            seedGeneratorStore.clearProcessing()
            seedGeneratorStore.clearError()
        }
        catch(error) { 
            seedGeneratorStore.clearProcessing()
            seedGeneratorStore.setError('Whoops! Something went wrong!')
            console.log(error) 
        }
    }

    async requestSeed(fileToUpload) {
        let formData = this.buildFormData(fileToUpload)

        const response = await fetch('api/seed', {
            method: 'POST',
            body: formData
        })

        const name = this.parseResponse(response, 'filename')
        const seed = this.parseResponse(response, 'seed')
        const file = await response.blob()

        seedGeneratorStore.setSeed(seed)

        this.setState({
            showDownload: true,
            romUri: window.URL.createObjectURL(file),
            romName: name,
        })  
    }

    async requestSpoiler() {
        const { seed } = seedGeneratorStore

        const response = await fetch(`api/seed/${seed}/spoiler`, {
            method: 'GET',
        })

        const file = await response.blob()
        const name = this.parseResponse(response, 'filename')

        this.setState({
            spoilerUri: window.URL.createObjectURL(file),
            spoilerName: name
        })
    }

    /*================================
        Button Handlers
    ================================*/

    handleSubmit(event) {
        event.preventDefault()
                
        if (this.fileInput.current.files.length === 0) {            
            seedGeneratorStore.setError('Hey, man. You need to upload a ROM file.')
            return
        }


        if (isNaN(seedGeneratorStore.seed) || seedGeneratorStore.seed < 0) {
            seedGeneratorStore.setError('Hey, man. You need to enter a valid non-negative integer for a seed!')
            return
        }

        if (seedGeneratorStore.goal === 'Dark Gaia') {
            if (isNaN(seedGeneratorStore.statues) || seedGeneratorStore.statues < 1 || seedGeneratorStore.statues > 6) {
                console.log(seedGeneratorStore.statues)
                seedGeneratorStore.setError('Hey, man. You need to enter a valid non-negative integer (between 1 and 6) for a statue count!')
                return
            }
        }
          
        const file = this.fileInput.current.files[0]
    
        this.generateSeed(file)
    }
    
    handleDownloadRom() {
        const { romUri, romName } = this.state
        
        var a = document.createElement('a')
            document.body.appendChild(a)
            a.style = 'display: none'
            a.href = romUri
            a.download = romName
            a.click()
            a.remove()
    }

    handleDownloadSpoiler() {
        const { spoilerUri, spoilerName } = this.state
    
        var a = document.createElement('a')
            document.body.appendChild(a)
            a.style = 'display: none'
            a.href = spoilerUri
            a.download = spoilerName
            a.click()
            a.remove()
    }

    handleRandomizeSeed() {
        const max = 2147483648
        const min = 0

        const seed = this.getRandomInRange(min, max)
        seedGeneratorStore.setSeed(seed)
    }

    render() {
        const { showDownload } = this.state

        return (
            <Container>
                <Card>
                    <CardBody>
                        <CardTitle>Rom Details</CardTitle>
                        <Row>
                        <Form>
                            <FormGroup>
                                <label> ROM File (*.sfc):<input required className="form-control" type="file" ref={this.fileInput} /></label>
                            </FormGroup>
                            <FormGroup>
                                <label> Seed:<FormInput value={seedGeneratorStore.seed} onChange={(e) => seedGeneratorStore.setSeed(e.target.value) } type="text" /></label>
                                <Button onClick={this.handleRandomizeSeed} style={{ marginLeft: 10 }}>Randomize Seed</Button>
                            </FormGroup>            
                            <Button type="submit" onClick={this.handleSubmit}>Generate ROM</Button>
                        </Form>
                </Row>
                { showDownload && (
                    <Row style={{marginTop: 20}}>
                        <Button onClick={this.handleDownloadRom}>Download Randomized ROM</Button>
                        <Button onClick={this.handleDownloadSpoiler} style={{ marginLeft: 10 }}>Download Spoiler Log</Button>
                    </Row>
                )}
                    </CardBody>
                </Card>
                
            </Container>            
        )
    }

    buildFormData(fileToUpload) {
        let formData = new FormData()
        formData.append(null, fileToUpload)
        formData.append('seed', seedGeneratorStore.seed === 0 ? null : seedGeneratorStore.seed)
        formData.append('difficulty', seedGeneratorStore.difficulty)
        formData.append('goal', seedGeneratorStore.goal)
        formData.append('variant', seedGeneratorStore.variant)
        formData.append('mode', seedGeneratorStore.mode)
        formData.append('firebird', seedGeneratorStore.firebird)
        
        if (seedGeneratorStore.goal === 'Dark Gaia') {
            let statues = seedGeneratorStore.statues

            if (seedGeneratorStore.statuesRandom) {
                statues = this.getRandomInRange(0, 6)
                console.log('Generating random statue count', statues)
            }

            formData.append('statues', statues)
        }           

        return formData
    }

    parseResponse(response, key) {
        var cd = response.headers.get('content-disposition')  

        var d = cd.split(';')

        for (let i = 0; i < d.length; ++i) {
            const idx = d[i].indexOf(key)

            if (idx > -1)                                
                return d[i].substring(idx + key.length + 1)             
        }
        
        return null
    }

    getRandomInRange(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min
    }
})

export default SeedGenerator