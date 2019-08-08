import React from 'react'
import {  Container } from 'shards-react'
import SeedDifficulty from './seed-difficulty';
import SeedGoal from './seed-goal';
import SeedVariant from './seed-variant';

export default class SeedOptions extends React.Component {
    render() {
        return (
            <Container>
                <SeedDifficulty />
                <SeedGoal />              
                <SeedVariant />
            </Container>
        )
    }
}