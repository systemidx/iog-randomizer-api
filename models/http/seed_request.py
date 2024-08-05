import json
import numbers
import random

from iog_randomizer.randomizer.models.enums import DarkRooms
from iog_randomizer.randomizer.models.enums import Difficulty
from iog_randomizer.randomizer.models.enums import Enemizer
from iog_randomizer.randomizer.models.enums import FluteOpt
from iog_randomizer.randomizer.models.enums import Goal
from iog_randomizer.randomizer.models.enums import Logic
from iog_randomizer.randomizer.models.enums import StartLocation
from iog_randomizer.randomizer.models.enums import StatueReq


class SeedRequest(object):
    schema = {
        'type': 'object',
        'properties': {
            'seed': {'type': 'number'},
            'difficulty': {'type': 'number'},
            'goal': {'type': 'number'},
            'logic': {'type': 'number'},
            'statues': {'type': 'string'},
            'statueReq': {'type': 'number'},
            'enemizer': {'type': 'number'},
            'startLocation': {'type': 'number'},
            'firebird': {'type': 'boolean'},
            'ohko': {'type': 'boolean'},
            'redJewelMadness': {'type': 'boolean'},
            'allowGlitches': {'type': 'boolean'},
            'bossShuffle': {'type': 'boolean'},
            'openMode': {'type': 'boolean'},
            'z3Mode': {'type': 'boolean'},
            'overworldShuffle': {'type': 'boolean'},
            'generateRaceRom': {'type': 'boolean'},
            'flute': {'type': 'number'},
            'sprite': {'type': 'number'},
            'dungeonShuffle': {'type': 'boolean'},
            'townShuffle': {'type': 'boolean'},
            'coupledExits': {'type': 'boolean'},
            'hideSettings': {'type': 'boolean'},
            'orbRando': {'type': 'boolean'},
            'darkRooms': {'type': 'number'},
            'cursedRooms': {'type': 'boolean'},
            'infiniteInventory': {'type': 'boolean'},
            'dsWarp': {'type': 'boolean'},
        },
        'required': []
    }

    seed = random.randrange(0, 9999999)
    difficulty = Difficulty.NORMAL
    goal = Goal.DARK_GAIA
    logic = Logic.COMPLETABLE
    statues = "Random"
    statue_req = StatueReq.GAME_CHOICE
    enemizer = Enemizer.NONE
    start_location = StartLocation.SOUTH_CAPE
    firebird = False
    ohko = False
    red_jewel_madness = False
    allow_glitches = False
    boss_shuffle = False
    open_mode = False
    z3_mode = False
    overworld_shuffle = False
    town_shuffle = False
    generate_race_rom = False
    dungeon_shuffle = False
    flute = FluteOpt.START
    sprite = 0
    hide_settings = False
    coupled_exits = False
    orb_rando = False
    darkrooms = DarkRooms.NONE
    infinite_inventory = False
    ds_warp = False

    def __init__(self, payload):
        print(payload)
        self._validateSeed(payload)
        self._validateDifficulty(payload)
        self._validateGoal(payload)
        self._validateStatueReq(payload)
        self._validateLogic(payload)
        self._validateEnemizer(payload)
        self._validateStartLocation(payload)
        self._validateFlute(payload)
        self._validateDarkRooms(payload)
        self._validateSwitches(payload)

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
            self._validateStatueReq(payload)
            self._validateStatues(payload)

    def _validateStatueReq(self, payload):
        statueReq = payload.get("statueReq")
        self.statue_req = StatueReq(statueReq)

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

    def _validateFlute(self, payload):
        flute_opt = payload.get("flute")
        self.flute = FluteOpt(flute_opt)

    def _validateDarkRooms(self, payload):
        dark_rooms = payload.get("darkRooms", 0)
        curses = payload.get("allowGlitches")
        if curses:
            self.darkrooms = DarkRooms(-dark_rooms)
        else:
            self.darkrooms = DarkRooms(dark_rooms)

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
        self.z3_mode = getSwitch(payload.get("z3Mode"))
        self.dungeon_shuffle = getSwitch(payload.get("dungeonShuffle"))
        self.overworld_shuffle = getSwitch(payload.get("overworldShuffle"))
        self.town_shuffle = getSwitch(payload.get("townShuffle"))
        self.coupled_exits = getSwitch(payload.get("coupledExits"))
        self.orb_rando = getSwitch(payload.get("orbRando"))
        self.generate_race_rom = getSwitch(payload.get("generateRaceRom"))
        self.hide_settings = getSwitch(payload.get("hideSettings"))
        self.infinite_inventory = getSwitch(payload.get("infiniteInventory"))
        self.ds_warp = getSwitch(payload.get("dsWarp"))

        if self.red_jewel_madness and self.ohko:
            raise ValueError("Can't have OHKO and Red Jewel Madness both flagged")

    # endregion

    def to_json(self):
        return json.dumps(self.__dict__)
