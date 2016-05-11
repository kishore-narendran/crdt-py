from flask import Blueprint, jsonify, request
from generate_key import generate_random_key


counter_api_blueprint = Blueprint('Counter', __name__)


@counter_api_blueprint.route("/g/new", methods=['GET'])
def new_g_counter():
    key = request.args.get('key')

    ##
    # If the key in request is empty or if there is no key in request

    if key is None or len(key) is 0:
        key = generate_random_key()

    ##
    # TODO - Creating, a new counter and inserting into redis

    result_dict = dict()
    result_dict['status'] = {'message': 'success', 'code': 0}
    result_dict['key'] = key

    return jsonify(result_dict)


@counter_api_blueprint.route("/g/update", methods=['GET'])
def update_g_counter_state():
    key = request.args.get('key')
    state = request.args.get('state')
    result_dict = dict()

    if key is None or state is None:
        result_dict['status'] = {'message': 'failure', 'code': 1,
                                 'notes': 'Key/State of counter was missing or malformed'}
    else:
        ##
        # TODO - Check for counter with given key, and if there is such a counter, perform merge

        result_dict['status'] = {'message': 'success', 'code': 1}

        ##
        # TODO - Return updated counter value
        result_dict['counter'] = 0

    return jsonify(result_dict)


@counter_api_blueprint.route("/pn/new", methods=['GET'])
def new_pn_counter():
    key = request.args.get('key')

    ##
    # If the key in request is empty or if there is no key in request

    if key is None or len(key) is 0:
        key = generate_random_key()

    ##
    # TODO - Creating, a new counter and inserting into redis

    result_dict = dict()
    result_dict['status'] = {'message': 'success', 'code': 0}
    result_dict['key'] = key

    return jsonify(result_dict)


@counter_api_blueprint.route("/pn/update", methods=['GET'])
def update_counter_state():
    key = request.args.get('key')
    state = request.args.get('state')
    result_dict = dict()

    if key is None or state is None:
        result_dict['status'] = {'message': 'failure', 'code': 1,
                                 'notes': 'Key/State of counter was missing or malformed'}
    else:
        ##
        # TODO - Check for counter with given key, and if there is such a counter, perform merge

        result_dict['status'] = {'message': 'success', 'code': 1}

        ##
        # TODO - Return updated counter value
        result_dict['counter'] = 0

    return jsonify(result_dict)
