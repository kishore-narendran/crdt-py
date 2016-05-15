from flask import Blueprint, jsonify, request

from constants import DATA_TYPES, G_COUNTER, CLIENTS
from generate_key import generate_random_key
from redis_manager import redis_manager
from status_codes import status_codes

counter_api_blueprint = Blueprint('Counter', __name__)


@counter_api_blueprint.route("/g/new", methods=['GET'])
def new_g_counter():
    key = request.args.get('key')
    clientid = request.args.get('clientid')
    val = request.args.get('val')
    ##
    # If the key in request is empty or if there is no key in request

    if key is None or len(key) is 0:
        key = generate_random_key()

    clients_list = CLIENTS + key
    cur_client = key + '_' + clientid

    ##
    #  Checking if the key is already present in Redis

    result_dict = dict()
    found_key_flag = redis_manager.hget(DATA_TYPES, key) is not None
    data_type_matched = (redis_manager.hget(DATA_TYPES, key) == G_COUNTER)
    if found_key_flag is False:
        add_client_g_counter(cur_client, clients_list, val)
        redis_manager.hset(DATA_TYPES, key, G_COUNTER)
        result_dict['status'] = status_codes['success']
        result_dict['key'] = key
        result_dict['counter'] = val
    elif found_key_flag is True and data_type_matched is True:
        add_client_g_counter(cur_client, clients_list, val)
        result_dict['status'] = status_codes['existing_key']
    else:
        result_dict['status'] = status_codes['data_type_mismatch']

    return jsonify(result_dict)


def add_client_g_counter(new_client, clients_list, val):
    for client in list(redis_manager.smembers(clients_list)):
        redis_manager.hset(client, new_client, val)

    redis_manager.sadd(clients_list, new_client)

    for client in list(redis_manager.smembers(clients_list)):
        redis_manager.hset(new_client, client, 0)

    redis_manager.hset(new_client, new_client, val)


@counter_api_blueprint.route("/g/update", methods=['GET'])
def update_g_counter_state():
    key = request.args.get('key')
    cur_client_id = request.args.get('clientid')
    val = request.args.get('val')

    cur_client = key + '_' + cur_client_id
    found_key_flag = redis_manager.hget(DATA_TYPES, key) is not None
    data_type_matched = (redis_manager.hget(DATA_TYPES, key) == G_COUNTER)

    result_dict = dict()

    ##
    # Checking if a valid key and state has been requested, and checking if
    # the key is present in the Redis key/value data store.

    if key is None or val is None:
        result_dict['status'] = status_codes['missing_key_or_state']
    elif found_key_flag is False:
        result_dict['status'] = status_codes['key_not_found']
    elif data_type_matched is False:
        result_dict['status'] = status_codes['data_type_mismatch']
    else:
        redis_manager.hset(cur_client, cur_client, val)
        result_dict['status'] = status_codes['success']

    return jsonify(result_dict)


@counter_api_blueprint.route("/g/get", methods=['GET'])
def get_g_counter():
    key = request.args.get('key')
    cur_client_id = request.args.get('clientid')

    clients_list = CLIENTS + key
    cur_client = key + '_' + cur_client_id

    counter = 0
    all_clients = list(redis_manager.smembers(clients_list))

    # TRIGGER MERGE to update state of this client
    g_counter_merge(cur_client, all_clients)

    # ADD up the counts of all clients
    for client in all_clients:
        counter += int(redis_manager.hget(cur_client, client))

    result_dict = dict()
    result_dict['status'] = status_codes['success']
    result_dict['counter'] = counter

    return jsonify(result_dict)


def g_counter_merge(cur_client, all_clients):
    cur_client_state = redis_manager.hgetall(cur_client)
    for client in all_clients:
        client_state = redis_manager.hgetall(client)
        for k, v in cur_client_state.items():
            cur_client_state[k] = max(int(v), int(client_state[k]))
    for k, v in cur_client_state.items():
        redis_manager.hset(cur_client, k, v)


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
