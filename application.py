import json, logging, sys

from flask import Flask, request, Response, make_response, jsonify, json
from flask_cors import CORS
from flask_expects_json import expects_json

from randomizer.iogr_rom import Randomizer, generate_filename
from randomizer.errors import FileNotFoundError
from randomizer.models.randomizer_data import RandomizerData

from requests.generate_seed_request import GenerateSeedRequest

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/v1/seed/generate": {"origins": "*"}})

@app.errorhandler(400)
def bad_request(errors):
    return make_response(jsonify({'errors': errors.description}), 400)


@app.route("/v1/seed/generate", methods=["POST"])
@expects_json(GenerateSeedRequest.schema)
def generateSeed(retries: int = 0) -> Response:
    logger = logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    
    if retries > 3:
        return make_response("Failed to generate a seed", 500)

    try:
        rom_path = "./data/gaia.bin"

        request_params = request.get_json()
        request_data = GenerateSeedRequest(request_params)
        logger.info(request_params)

        settings = RandomizerData(request_data.seed, request_data.difficulty, request_data.goal,
                                  request_data.logic, request_data.statues, request_data.enemizer, request_data.start_location,
                                  request_data.firebird, request_data.ohko)

        rom_filename = generate_filename(settings, "sfc")
        spoiler_filename = generate_filename(settings, "json")

        randomizer = Randomizer(rom_filename, rom_path, settings)

        patch = randomizer.generate_rom()
        spoiler = randomizer.generate_spoiler()

        return make_response(json.dumps({'patch': patch, 'spoiler': spoiler}), 200)
    except ValueError as e:
        return make_response(str(e.args), 400)
    except FileNotFoundError:
        return make_response(404)
    except Exception as e:
        return generateSeed(retries + 1)


if __name__ == "__main__":
    app.run(debug=True)
