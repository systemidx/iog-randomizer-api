import detailsStore from '../../stores/details'
import enemizerStore from '../../stores/enemizer'
import entranceStore from '../../stores/entrance'
import variantsStore from '../../stores/variants'
import uiStore from '../../stores/ui'

class SeedService {
    async requestSeed() {        
        let formData = this.buildFormData(detailsStore.file)

        const response = await fetch('api/seed', {
            method: 'POST',
            body: formData
        })

        const name = this.parseResponse(response, 'filename')
        const seed = this.parseResponse(response, 'seed')
        const file = await response.blob()

        detailsStore.setSeed(seed)
                
        uiStore.setRomURI(window.URL.createObjectURL(file))
        uiStore.setRomName(name)
    }

    async requestSpoiler() {
        const { seed } = detailsStore

        const response = await fetch(`api/seed/${seed}/spoiler`, {
            method: 'GET',
        })

        if (!response || !response.headers)
            return null

        const file = await response.blob()
        const name = this.parseResponse(response, 'filename')

        uiStore.setSpoilerUri(window.URL.createObjectURL(file))
        uiStore.setSpoilerName(name)
    }

    buildFormData(file) {
        let formData = new FormData()

        formData.append(null, file)
        formData.append('seed', detailsStore.seed === 0 ? null : detailsStore.seed)
        formData.append('difficulty', detailsStore.difficulty)
        formData.append('goal', detailsStore.goal)
        if (detailsStore.goal === 'Dark Gaia')
            formData.append('statues', detailsStore.statues)

        formData.append('startLocation', variantsStore.startLocation)
        formData.append('logic', variantsStore.logic)
        formData.append('allowGlitches', variantsStore.allowGlitches)
        formData.append('oneHitKnockOut', variantsStore.oneHitKnockOut)
        formData.append('redJewelMadness', variantsStore.redJewelMadness)
        formData.append('firebird', variantsStore.firebird)

        formData.append('enemizer', enemizerStore.enemizer)
        formData.append('bossShuffle', enemizerStore.bossShuffle)

        formData.append('entranceShuffle', entranceStore.entranceShuffle)
        formData.append('dungeonShuffle', entranceStore.dungeonShuffle)
        formData.append('overworldShuffle', entranceStore.overworldShuffle)

        return formData
    }

    parseResponse(response, key) {
        let cd = response.headers.get('content-disposition')
        let d = cd.split(';')

        for (let i = 0; i < d.length; ++i) {
            const idx = d[i].indexOf(key)

            if (idx > -1)
                return d[i].substring(idx + key.length + 1)
        }

        return null
    }
}

const seedService = new SeedService()
export default seedService