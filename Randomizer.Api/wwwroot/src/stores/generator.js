import {  observable, action, decorate } from 'mobx'


class SeedGeneratorStore {
    isProcessing = false
    isError = false    
    errorText = null
    difficulty = 'Normal'
    goal = 'Dark Gaia'
    variant = 'None'
    mode = 'Completable'
    firebird = false
    seed = 0
    statues = 4

    setError = action('setError', (text) => {
        this.isError = true
        this.errorText = text
    })

    clearError = action('clearError', () => {
        this.isError = false
    })

    setProcessing = action('setProcessing', () => {
        this.isProcessing = true
    })    

    clearProcessing = action('clearProcessing', () => {
        this.isProcessing = false
    })

    setSeed = action('setSeed', (seed) => {
        this.seed = seed
    })
    
    setDifficulty = action('setDifficulty', (difficulty) => {        
        this.difficulty = difficulty
    })

    setGoal = action('setGoal', (goal) => {
        this.goal = goal
    })

    setVariant = action('setVariant', (variant) => {
        this.variant = variant
    })

    setMode = action('setMode', (mode) => {
        this.mode = mode
    })

    setFirebird = action('setFirebird', (firebird) => {
        this.firebird = firebird
    })

    setStatues = action('setStatues', (statues) => {
        this.statues = statues
    })
}

decorate(SeedGeneratorStore, {
    isProcessing: observable,
    isError: observable,
    errorText: observable,
    seed: observable,
    difficulty: observable,
    goal: observable,
    mode: observable,
    variant: observable,
    firebird: observable,
    statues: observable
})

const seedGeneratorStore = new SeedGeneratorStore()
export default seedGeneratorStore