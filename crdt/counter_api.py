from flask import Blueprint, jsonify, request
from generate_key import generate_random_key
from redis_manager import redis_manager
from status_codes import status_codes


counter_api_blueprint = Blueprint('Counter', __name__)


@counter_api_blueprint.route("/g/new", methods=['GET'])
def new_g_counter():
    key = request.args.get('key')
    ##
    # If the key in request is empty or if there is no key in request

    if key is None or len(key) is 0:
        key = generate_random_key()

    ##
    #  Checking if the key is already present in Redis

    result_dict = dict()
    found_key_flag = redis_manager.get(key) is not None
    if found_key_flag is False:
        redis_manager.set(key, 0)
        result_dict['status'] = status_codes['success']
        result_dict['key'] = key
        result_dict['counter'] = 0
    else:
        result_dict['status'] = status_codes['existing_key']

    return jsonify(result_dict)


@counter_api_blueprint.route("/g/update", methods=['GET'])
def update_g_counter_state():
    key = request.args.get('key')
    state = request.args.get('state')

    found_key_flag = redis_manager.get(key) is not None
    result_dict = dict()

    ##
    # Checking if a valid key and state has been requested, and checking if
    # the key is present in the Redis key/value data store. If both these
    # conditions are met then the merge operation is performed

    if key is None or state is None:
        result_dict['status'] = status_codes['missing_key_or_state']
    elif found_key_flag is False:
        result_dict['status'] = status_codes['key_not_found']
    else:
        ##
        # TODO - Check for counter with given key, and if there is such a counter, perform merge

        result_dict['status'] = status_codes['success']

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
    #  Checking if the key is already present in Redis

    result_dict = dict()
    found_key_flag = redis_manager.get(key) is not None
    if found_key_flag is False:
        redis_manager.set(key, 0)
        result_dict['status'] = status_codes['success']
        result_dict['key'] = key
        result_dict['counter'] = 0
    else:
        result_dict['status'] = status_codes['existing_key']

    return jsonify(result_dict)


@counter_api_blueprint.route("/pn/update", methods=['GET'])
def update_pn_counter_state():
    key = request.args.get('key')
    state = request.args.get('state')

    found_key_flag = redis_manager.get(key) is not None
    result_dict = dict()

    ##
    # Checking if a valid key and state has been requested, and checking if
    # the key is present in the Redis key/value data store. If both these
    # conditions are met then the merge operation is performed

    if key is None or state is None:
        result_dict['status'] = status_codes['missing_key_or_state']
    elif found_key_flag is False:
        result_dict['status'] = status_codes['key_not_found']
    else:
        ##
        # TODO - Check for counter with given key, and if there is such a counter, perform merge

        result_dict['status'] = status_codes['success']

        ##
        # TODO - Return updated counter value
        result_dict['counter'] = 0

    return jsonify(result_dict)
