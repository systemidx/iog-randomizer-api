import React, { Fragment } from 'react';

import { Container, Row, Col, Modal, ModalHeader, ModalBody } from "shards-react";

import { FaBomb } from 'react-icons/fa'
import ClipLoader from 'react-spinners/ClipLoader'


import Navigation from './components/navigation'
import SeedGenerator from './components/seed-generator'

import { observer } from 'mobx-react'
import seedGeneratorStore from './stores/generator'
import SeedOptions from './components/seed-options';

const App = observer(
  class App extends React.Component {
    state = {
      isProcessing: false,
      isError: false,
      
    }

    constructor(props) {
      super(props)

      
      this.clearError = this.clearError.bind(this)    
    }

    

    clearError() {
      seedGeneratorStore.setError(false)
    }


    render() {
      const { isError, isProcessing } = seedGeneratorStore

      return (      
        <Fragment>
          <Navigation />
          <Container>
            <Row style={{ marginTop: 20}}>
              <Col><SeedGenerator /></Col>
              <Col><SeedOptions /></Col>
            </Row>
          </Container>
          { isError && (
            <Modal open={isError} toggle={this.clearError}>
              <ModalHeader>Whoops</ModalHeader>
              <ModalBody><FaBomb color="red" style={{ verticalAlign: 'center' }} /> Hey, man. You need to upload a ROM file.</ModalBody>
            </Modal>
          )}
          { isProcessing && (
            <Modal open={isProcessing} toggle={() => {}}>
            <ModalHeader>Generating Seed</ModalHeader>
            <ModalBody>
              <div style={{flex: 1, justifyContent: 'center', alignContent: 'center'}}>
                <ClipLoader sizeUnit={"px"} size={150} color={'#123abc'} loading={true} />
                <span>Loading...</span>
              </div>
              </ModalBody>
          </Modal>
          )}
        </Fragment>
      );
    }
  }
)

export default App