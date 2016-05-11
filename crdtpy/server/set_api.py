from flask import Blueprint, jsonify, request
from generate_key import generate_random_key


set_api_blueprint = Blueprint('Set', __name__)


@set_api_blueprint.route("/g/new", methods=['GET'])
def new_g_set():
    key = request.args.get('key')

    ##
    # If the key in request is empty or if there is no key in request

    if key is None or len(key) is 0:
        key = generate_random_key()

    ##
    # TODO - Creating, a new set and inserting into redis

    result_dict = dict()
    result_dict['status'] = {'message': 'success', 'code': 0}
    result_dict['key'] = key
    result_dict['set'] = []

    return jsonify(result_dict)


@set_api_blueprint.route("/g/update", methods=['GET'])
def update_g_counter_state():
    key = request.args.get('key')
    state = request.args.get('state')
    result_dict = dict()

    if key is None or state is None:
        result_dict['status'] = {'message': 'failure', 'code': 1,
                                 'notes': 'Key/State of counter was missing or malformed'}
    else:
        ##
        # TODO - Check for set with given key, and if there is such a set, perform merge

        result_dict['status'] = {'message': 'success', 'code': 1}

        ##
        # TODO - Return updated set
        result_dict['state'] = []

    return jsonify(result_dict)


@set_api_blueprint.route("/2p/new", methods=['GET'])
def new_pn_counter():
    key = request.args.get('key')

    ##
    # If the key in request is empty or if there is no key in request

    if key is None or len(key) is 0:
        key = generate_random_key()

    ##
    # TODO - Creating, a new set and inserting into redis

    result_dict = dict()
    result_dict['status'] = {'message': 'success', 'code': 0}
    result_dict['key'] = key
    result_dict['set'] = []

    return jsonify(result_dict)


@set_api_blueprint.route("/2p/update", methods=['GET'])
def update_counter_state():
    key = request.args.get('key')
    state = request.args.get('state')
    result_dict = dict()

    if key is None or state is None:
        result_dict['status'] = {'message': 'failure', 'code': 1,
                                 'notes': 'Key/State of counter was missing or malformed'}
    else:
        ##
        # TODO - Check for set with given key, and if there is such a set, perform merge

        result_dict['status'] = {'message': 'success', 'code': 1}

        ##
        # TODO - Return updated set value
        result_dict['set'] = []

    return jsonify(result_dict)
