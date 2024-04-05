import logging, time, json

from flask import Flask, request, Response, make_response
from flask_cors import CORS
from flask_expects_json import expects_json

from randomizer.iogr_rom import Randomizer, generate_filename, VERSION
from randomizer.models.randomizer_data import RandomizerData as Settings
from randomizer.models.enums import EntranceShuffle, FluteOpt   # legacy

from config import Config
from database import Database

from encoder import JSONEncoder
from models.http.seed_request import SeedRequest
from models.http.seed_response import SeedResponse
from models.http.version_response import VersionResponse
from models.patch import Patch
from models.spoiler import Spoiler
from models.result import Result

logging.basicConfig(level=logging.DEBUG, filename="output.log")

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.json_encoder = JSONEncoder

cors = CORS(app, resources={
    r"/v1/*": {"origins": "*"}
})

config = Config()
database = Database(logging, config)

@app.route("/v1/seed/generate", methods=["POST"])
@expects_json(SeedRequest.schema)
def generateSeed() -> Response:
    request_data = SeedRequest(request.get_json())
    settings = Settings(seed = request_data.seed, 
                        difficulty = request_data.difficulty, goal = request_data.goal, logic = request_data.logic, 
                        statues = request_data.statues, statue_req = request_data.statue_req,
                        firebird = request_data.firebird, ohko = request_data.ohko, z3 = request_data.z3_mode,
                        red_jewel_madness = request_data.red_jewel_madness, allow_glitches = request_data.allow_glitches, 
                        open_mode = request_data.open_mode, race_mode = request_data.generate_race_rom,
                        start_location = request_data.start_location, 
                        enemizer = request_data.enemizer, 
                        boss_shuffle = request_data.boss_shuffle, 
                        overworld_shuffle = request_data.overworld_shuffle, 
                        coupled_exits = False if request_data.entrance_shuffle == EntranceShuffle.UNCOUPLED else True,
                        town_shuffle = False if request_data.entrance_shuffle == EntranceShuffle.NONE else True,
                        flute = FluteOpt.FLUTELESS if request_data.fluteless else FluteOpt.START
                        )

    randomizer = Randomizer("./data/gaia.bin")
    result = __generate(randomizer, settings, request_data.generate_race_rom, 0, request_data.hide_settings)
    if result is None:
        return make_response("Failed to generate a seed", 500)

    if result.patch is None:
        return make_response("Failed to generate a seed", 500)

    patch = result.patch
    spoiler = result.spoiler
    permalink = result.permalink

    response = SeedResponse(patch.patch, patch.patchName, patch.version, permalink)
    if spoiler is not None:
        response.spoiler = spoiler.spoiler
        response.spoilerName = spoiler.spoilerName

    if permalink is not None:
        response.permalink_id = permalink

    return make_response(response.to_json(), 200)


@app.route("/v1/seed/permalink/<link_id>", methods=["GET"])
def getPermalinkedSeed(link_id: str = "") -> Response:
    try:
        if link_id == "":
            return make_response("Did not send permalink ID", 401)

        logging.info("Attempting to get permalink: " + link_id)
        document = database.get(link_id)
        if document is None:
            return make_response("Permalink Not Found", 404)

        return make_response(json.dumps(document, cls=JSONEncoder), 200)
    except Exception as e:
        logging.exception(e)
        return make_response("An unknown error has occurred", 500)


@app.route("/v1/api/version", methods=["GET"])
def getRandomizerVersion() -> Response:
    version = VersionResponse(VERSION)
    return make_response(version.to_json())


def __generate(randomizer: Randomizer, settings: Settings, race: bool = False, retries: int = 0, hide_settings: bool = False) -> Result:
    if retries >= 3:
        return None

    patch = None
    permalink = None
    spoiler = None

    try:
        patch_start_time = time.perf_counter()
        logging.info(f"({settings.seed}) Generating patch ({retries + 1} / 3)...")
        logging.info(f"({settings.seed}) Settings: {str(request.get_json())}")

        patch = __generatePatch(randomizer, settings, hide_settings)
        if patch is None:
            logging.info(f"({settings.seed}) Failed to generate patch in {time.perf_counter() - patch_start_time} seconds!")
            return __generate(randomizer, settings, race, retries + 1, hide_settings)
        else:
            logging.info(f"({settings.seed}) Generated patch in {time.perf_counter() - patch_start_time} seconds!")

        if not race:
            logging.info(f"({settings.seed}) Race Mode off, generating spoiler...")
            spoiler_start_time = time.perf_counter()
            spoiler = __generateSpoiler(randomizer, settings, hide_settings)
            logging.info(f"({settings.seed}) Generated spoiler in {time.perf_counter() - spoiler_start_time} seconds!")
        else:
            logging.info(f"({settings.seed}) Race Mode on, not generating spoiler...")

        if database.enabled:
            logging.info(f"({settings.seed}) Generating permalink...")
            permalink_start_time = time.perf_counter()
            permalink = database.create(patch, spoiler, settings, hide_settings)
            logging.info(
                f"({settings.seed}) Permalink generated in {time.perf_counter() - permalink_start_time} seconds!")

        return Result(patch, spoiler, permalink)

    except Exception as e:
        logging.exception(e)
        return __generate(randomizer, settings, race, retries + 1, hide_settings)


def __generateFileName(settings: Settings, extension: str, obfuscate_options: bool = False) -> str:
    if obfuscate_options:
        file_name = "IoGR_V" + VERSION + "_" + str(settings.seed) + "." + extension
        return file_name
    return generate_filename(settings, extension)


def __generatePatch(randomizer: Randomizer, settings: Settings, hide_settings: bool = False) -> Patch:
    patch_filename = __generateFileName(settings, "sfc", hide_settings)
    patch = randomizer.generate_legacy_patch(patch_filename, settings)
    return Patch(patch, patch_filename, VERSION)


def __generateSpoiler(randomizer: Randomizer, settings: Settings, hide_settings: bool = False) -> Spoiler:
    spoiler_filename = __generateFileName(settings, "txt", hide_settings)
    spoiler = randomizer.generate_spoiler()
    return Spoiler(spoiler, spoiler_filename)


if __name__ == "__main__":
    app.debug = config.DEBUG
    app.run(host="0.0.0.0", port=5000)
