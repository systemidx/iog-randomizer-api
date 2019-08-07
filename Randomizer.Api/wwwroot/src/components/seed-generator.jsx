import React from 'react'
import { Button, Card, CardBody, CardTitle, Container, Form, FormInput, FormGroup, Row } from "shards-react";

import seedGeneratorStore from '../stores/generator'
import SeedOptions from './seed-options';

export default class SeedGenerator extends React.Component {
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
        this.upload = this.upload.bind(this)

        this.fileInput = React.createRef();
        this.seedInput = React.createRef();
    }

    async upload(fileToUpload) {
        seedGeneratorStore.setProcessing()

        let formData = this.buildFormData(fileToUpload)

        try {
            const response = await fetch('api/seed', {
                method: 'POST',
                body: formData
            })

            const { name, file } = await this.parseResponse(response)
    
            seedGeneratorStore.clearProcessing()
            seedGeneratorStore.clearError()

            this.setState({
                showDownload: true,
                romUri: window.URL.createObjectURL(file),
                romName: name,
            })  
        }
        catch(error) { 
            seedGeneratorStore.clearProcessing()
            seedGeneratorStore.clearError()
            console.log(error) 
        }
    }

    handleSubmit(event) {
        event.preventDefault()
                
        if (this.fileInput.current.files.length === 0) {            
            seedGeneratorStore.setError('Hey, man. You need to upload a ROM file.')
            return
        }
          
        const file = this.fileInput.current.files[0]
    
        this.upload(file)
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
                            <label> ROM File (*.sfc):
                                <input required className="form-control" type="file" ref={this.fileInput} />          
                            </label>
                            </FormGroup>
                            <FormGroup>
                                <label> Seed:
                                <FormInput placeholder="123456" onChange={(e) => seedGeneratorStore.setSeed(e.target.value) } type="number" min="0" />
                                </label>
                            </FormGroup>            
                            <Button type="submit" onClick={this.handleSubmit}>Generate ROM</Button>
                        </Form>
                </Row>
                { showDownload && (
                    <Row style={{marginTop: 20}}>
                        <Button onClick={this.handleDownloadRom}>Download Randomized ROM</Button>
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
        formData.append('seed', seedGeneratorStore.seed)
        formData.append('difficulty', seedGeneratorStore.difficulty)
        formData.append('goal', seedGeneratorStore.goal)
        formData.append('variant', seedGeneratorStore.variant)
        formData.append('firebird', seedGeneratorStore.firebird)

        return formData
    }

    async parseResponse(response) {
        var cd = response.headers.get('content-disposition')  
        var idx = cd.indexOf('filename=') + 9
        
        var name = cd.substring(idx)  
        var file = await response.blob()  

        return { name, file }
    }
}