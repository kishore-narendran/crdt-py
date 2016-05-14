from flask import Blueprint, jsonify, request
from generate_key import generate_random_key
from redis_manager import redis_manager
from status_codes import status_codes
from constants import DATA_TYPES, G_COUNTER

counter_api_blueprint = Blueprint('Counter', __name__)


@counter_api_blueprint.route("/g/new", methods=['GET'])
def new_g_counter():
    key = request.args.get('key')
    clientid = request.args.get('clientid')
    val = request.args.get('val')
    print key, clientid
    ##
    # If the key in request is empty or if there is no key in request

    if key is None or len(key) is 0:
        key = generate_random_key()

    clients_list = 'random'+key
    client_key = key + '_' + clientid

    print client_key, ' = client key'
    ##
    #  Checking if the key is already present in Redis

    result_dict = dict()
    found_key_flag = redis_manager.get(key) is not None
    data_type_matched = redis_manager.hget(DATA_TYPES, key) is G_COUNTER
    if found_key_flag is False:
        # redis_manager.set(key, val)
        add_client_g_counter(client_key, clients_list, val)
        redis_manager.hset(DATA_TYPES, key, G_COUNTER)
        result_dict['status'] = status_codes['success']
        result_dict['key'] = key
        result_dict['counter'] = val
    elif found_key_flag is True and data_type_matched is True:
        add_client_g_counter(client_key, clients_list, val)
        result_dict['status'] = status_codes['existing_key']
    else:
        result_dict['status'] = status_codes['data_type_mismatch']

    return jsonify(result_dict)


def add_client_g_counter(new_client, clients_list, val):
    lock = redis_manager.lock(clients_list)

    if lock.acquire(blocking=False):
        for client in list(redis_manager.smembers(clients_list)):
            redis_manager.hset(client, new_client, val)
        redis_manager.sadd(clients_list, new_client)

        for client in list(redis_manager.smembers(clients_list)):
            redis_manager.hset(new_client, client, 0)

        redis_manager.hset(new_client, new_client, val)


@counter_api_blueprint.route("/g/update", methods=['GET'])
def update_g_counter_state():
    key = request.args.get('key')
    clientid = request.args.get('clientid')
    val = request.args.get('state')

    client_key = key + '_' + clientid

    found_key_flag = redis_manager.get(key) is not None
    data_type_matched = redis_manager.hget(DATA_TYPES, key) is G_COUNTER

    result_dict = dict()

    ##
    # Checking if a valid key and state has been requested, and checking if
    # the key is present in the Redis key/value data store.

    if key is None or state is None:
        result_dict['status'] = status_codes['missing_key_or_state']
    elif found_key_flag is False:
        result_dict['status'] = status_codes['key_not_found']
    elif data_type_matched is False:
        result_dict['status'] = status_codes['data_type_mismatch']
    else:
        ##
        # TODO - update the state of current client
        redis_manager.hset(client_key, client_key, val)
        result_dict['status'] = status_codes['success']

    return jsonify(result_dict)


@counter_api_blueprint.route("/g/get", methods=['GET'])
def get_g_counter():
    key = request.args.get('key')
    clientid = request.args.get('clientid')

    clients_list = key + '_' + 'clients'
    client_key = key + '_' + clientid

    no_of_clients = redis_manager.scard(clients_list)
    counter = 0
    for index in xrange(no_of_clients):
        counter += int(redis_manager.hget(client_key, redis_manager.lindex(clients_list, index)))

    result_dict = dict()
    result_dict['status'] = status_codes['success']
    result_dict['counter'] = counter

    # TODO - Lazy Merge: spawn a thread, asynchronously assign it a task to get all
    # TODO - the other client states to merge with current client state.

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
