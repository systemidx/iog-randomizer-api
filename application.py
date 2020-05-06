import json, logging, sys, hashlib, uuid, datetime

from flask import Flask, request, Response, make_response, jsonify, json
from flask_cors import CORS
from flask_expects_json import expects_json, ValidationError

from randomizer.iogr_rom import Randomizer, generate_filename, VERSION
from randomizer.errors import FileNotFoundError
from randomizer.models.randomizer_data import RandomizerData as Settings

from config import Config
from database import Database

from encoder import JSONEncoder
from models.http.seed_request import SeedRequest
from models.http.seed_response import SeedResponse
from models.http.version_response import VersionResponse
from models.patch import Patch
from models.spoiler import Spoiler

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.json_encoder = JSONEncoder

cors = CORS(app, resources={
    r"/v1/*": {"origins": "*"}
})

randomizer = Randomizer("./data/gaia.bin")
config = Config()
database = Database(logging, config)

@app.route("/v1/seed/generate", methods=["POST"])
@expects_json(SeedRequest.schema)
def generateSeed(retries: int = 0) -> Response:
    if retries > 3:
        return make_response("Failed to generate a seed", 500)

    try:
        request_data = SeedRequest(request.get_json())
        settings = Settings(request_data.seed, request_data.difficulty, request_data.goal, request_data.logic, request_data.statues, request_data.enemizer, request_data.start_location, request_data.firebird, request_data.ohko, request_data.red_jewel_madness, request_data.allow_glitches, request_data.boss_shuffle, request_data.open_mode, request_data.sprite)
        patch = __generatePatch(settings)

        if not request_data.generate_race_rom:            
            spoiler = __generateSpoiler(settings)
        else:
            spoiler = None

        if database.enabled:
            permalink_id = database.create(patch, spoiler, settings)
        else:
            permalink_id = None

        response = SeedResponse(patch.patch, patch.patchName, patch.version, permalink_id)
        if not request_data.generate_race_rom:
            response.spoiler = spoiler.spoiler
            response.spoilerName = spoiler.spoilerName

        return make_response(response.to_json(), 200)
    except ValueError as e:
        return make_response(str(e.args), 400)
    except FileNotFoundError:
        return make_response(404)
    except RecursionError:
        return generateSeed(retries + 1)
    except Exception as e:
        logging.exception("An unknown error has occurred")
        return generateSeed(retries + 1)

@app.route("/v1/seed/permalink/<link_id>", methods=["GET"])
def getPermalinkedSeed(link_id: str = "") -> Response:
    try:
        document = database.get(link_id)
        if document == None:
            return make_response("Permalink Not Found", 404)

        return make_response(document, 200)
    except Exception as e:
        logging.exception("An unknown error has occurred")
        return make_response("An unknown error has occurred", 500)

@app.route("/v1/api/version", methods=["GET"])
def getRandomizerVersion() -> Response:
    version = VersionResponse(VERSION)
    return make_response(version.to_json())

def __generatePatch(settings: Settings) -> Patch:
    patch_filename = generate_filename(settings, "sfc")
    patch = randomizer.generate_rom(patch_filename, settings)
    return Patch(patch, patch_filename, VERSION)

def __generateSpoiler(settings: Settings) -> Spoiler:
    spoiler_filename = generate_filename(settings, "txt")
    spoiler = randomizer.generate_spoiler()
    return Spoiler(spoiler, spoiler_filename)

if __name__ == "__main__":
    app.run(debug=True)
