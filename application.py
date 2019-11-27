import json, logging, sys

from flask import Flask, request, Response, make_response, jsonify, json
from flask_cors import CORS
from flask_expects_json import expects_json, ValidationError

from randomizer.iogr_rom import Randomizer, generate_filename
from randomizer.errors import FileNotFoundError
from randomizer.models.randomizer_data import RandomizerData

from requests.generate_seed_request import GenerateSeedRequest

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/v1/seed/generate": {"origins": "*"}})
logging.basicConfig(level=logging.DEBUG)
randomizer = Randomizer("./data/gaia.bin")


@app.route("/v1/seed/generate", methods=["POST"])
@expects_json(GenerateSeedRequest.schema)
def generateSeed(retries: int = 0) -> Response:
    if retries > 3:
        return make_response("Failed to generate a seed", 500)

    try:
        request_params = request.get_json()
        logging.debug(request_params)

        request_data = GenerateSeedRequest(request_params)
        response = __generate(request_data)

        return make_response(response, 200)
    except ValueError as e:
        return make_response(str(e.args), 400)
    except FileNotFoundError:
        return make_response(404)
    except RecursionError:
        return generateSeed(retries + 1)
    except Exception as e:
        logging.exception("An unknown error has occurred")
        return generateSeed(retries + 1)

def __generate(request: GenerateSeedRequest):
    settings = RandomizerData(request.seed, request.difficulty, request.goal, request.logic, request.statues, request.enemizer, request.start_location, request.firebird, request.ohko, request.red_jewel_madness, request.allow_glitches, request.boss_shuffle)
    payload = {}

    payload.update(__generatePatch(settings))
    if not request.generate_race_rom:
        payload.update(__generateSpoiler(settings))

    return json.dumps(payload)

def __generatePatch(settings: RandomizerData):      
    patch_filename = generate_filename(settings, "sfc") 
    patch = randomizer.generate_rom(patch_filename, settings)    

    return { 'patch': patch, 'patchName': patch_filename}

def __generateSpoiler(settings: RandomizerData):
    spoiler_filename = generate_filename(settings, "json")
    spoiler = randomizer.generate_spoiler()

    return { 'spoiler': spoiler, 'spoilerFilename': spoiler_filename }

if __name__ == "__main__":
    app.run(debug=True)
