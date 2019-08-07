import {  observable, action, decorate } from 'mobx'


class SeedGeneratorStore {
    isProcessing = false
    isError = false    
    difficulty = 'normal'
    goal = 'Dark Gaia'
    variant = 'None'
    firebird = false
    seed = 0

    setError = action('setError', (val) => {
        this.isError = val
    })

    setProcessing = action('setProcessing', (val) => {
        this.isProcessing = val
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

    setFirebird = action('setFirebird', (firebird) => {
        this.firebird = firebird
    })
}

decorate(SeedGeneratorStore, {
    isProcessing: observable,
    isError: observable,
    seed: observable,
    difficulty: observable,
    goal: observable,
    variant: observable,
    firebird: observable
})

const seedGeneratorStore = new SeedGeneratorStore()
export default seedGeneratorStore