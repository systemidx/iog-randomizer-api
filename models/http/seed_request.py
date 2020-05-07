import json
import random
import numbers

from randomizer.models.enums.difficulty import Difficulty
from randomizer.models.enums.goal import Goal
from randomizer.models.enums.logic import Logic
from randomizer.models.enums.enemizer import Enemizer
from randomizer.models.enums.start_location import StartLocation
from randomizer.models.enums.entrance_shuffle import EntranceShuffle
from randomizer.models.enums.sprites import Sprite

class SeedRequest(object):
    schema = {
        'type': 'object',
        'properties': {
            'seed': {'type': 'number'},
            'difficulty': {'type': 'number'},
            'logic': {'type': 'number'},
            'goal': {'type': 'number'},
            'statues': {'type': 'string'},
            'enemizer': {'type': 'number'},
            'startLocation': {'type': 'number'},
            'allowGlitches': {'type': 'boolean'},
            'ohko': {'type': 'boolean'},
            'redJewelMadness': {'type': 'boolean'},
            'firebird': {'type': 'boolean'},
            'bossShuffle': {'type': 'boolean'},
            'openMode': {'type': 'boolean'},
            'dungeonShuffle': {'type': 'boolean'},
            'overworldShuffle': {'type': 'boolean'},
            'generateRaceRom': {'type': 'boolean'},
            'sprite': {'type': 'string'}
        },
        'required': []
    }

    seed = random.randrange(0, 9999999)
    difficulty = Difficulty.NORMAL
    goal = Goal.DARK_GAIA
    statues = "Random"
    logic = Logic.COMPLETABLE
    enemizer = Enemizer.NONE
    start_location = StartLocation.SOUTH_CAPE
    entrance_shuffle = EntranceShuffle.NONE
    allow_glitches = False
    ohko = False
    red_jewel_madness = False
    firebird = False
    boss_shuffle = False
    open_mode = False
    dungeon_shuffle = False
    overworld_shuffle = False
    generate_race_rom = False
    sprite = Sprite.WILL

    def __init__(self, payload):
        self._validateSeed(payload)
        self._validateDifficulty(payload)
        self._validateGoal(payload)
        self._validateLogic(payload)
        self._validateEnemizer(payload)
        self._validateStartLocation(payload)
        self._validateEntranceShuffle(payload)
        self._validateSwitches(payload)
        self._validateSprite(payload)

    # region Validation Methods
    def _validateSeed(self, payload):
        seed = payload.get("seed")

        if isinstance(seed, numbers.Number) and seed > -1:
            self.seed = seed

    def _validateDifficulty(self, payload):
        difficulty = payload.get("difficulty")
        self.difficulty = Difficulty(difficulty)

    def _validateGoal(self, payload):
        goal = payload.get("goal")
        self.goal = Goal(goal)

        if self.goal != Goal.RED_JEWEL_HUNT:
            self._validateStatues(payload)

    def _validateSprite(self, payload):
        sprite = payload.get("sprite")
        if sprite is None:
            return
        
        self.sprite = Sprite(sprite.lower())

    def _validateStatues(self, payload):
        statues = payload.get("statues")

        if statues is not None:
            if statues.lower() == "random":
                self.statues = statues
            else:
                count = int(statues)
                if 0 <= count <= 6:
                    self.statues = statues
                else:
                    self.statues = "4"

    def _validateLogic(self, payload):
        logic = payload.get("logic")
        self.logic = Logic(logic)

    def _validateEnemizer(self, payload):
        enemizer = payload.get("enemizer")
        self.enemizer = Enemizer(enemizer)

    def _validateStartLocation(self, payload):
        start_location = payload.get("startLocation")
        self.start_location = StartLocation(start_location)

    def _validateEntranceShuffle(self, payload):
        entrance_shuffle = payload.get("entranceShuffle")
        self.entrance_shuffle = EntranceShuffle(entrance_shuffle)

    def _validateSwitches(self, payload):
        def getSwitch(switch):
            if switch is None:
                return False
            return switch

        self.allow_glitches = getSwitch(payload.get("allowGlitches"))
        self.ohko = getSwitch(payload.get("ohko"))
        self.red_jewel_madness = getSwitch(payload.get("redJewelMadness"))
        self.firebird = getSwitch(payload.get("firebird"))
        self.boss_shuffle = getSwitch(payload.get("bossShuffle"))
        self.open_mode = getSwitch(payload.get("openMode"))
        self.dungeon_shuffle = getSwitch(payload.get("dungeonShuffle"))
        self.overworld_shuffle = getSwitch(payload.get("overworldShuffle"))
        self.generate_race_rom = getSwitch(payload.get("generateRaceRom"))

        if self.red_jewel_madness and self.ohko:
            raise ValueError("Can't have OHKO and Red Jewel Madness both flagged")    

    # endregion

    def to_json(self):
        return json.dumps(self.__dict__)
