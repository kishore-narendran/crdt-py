import hot_redis
from flask import Blueprint, request, jsonify

from crdt.constants import DATA_TYPES, G_COUNTER, ALL_CLIENTS, PN_COUNTER
from crdt.generate_key import generate_random_crdt_key
from crdt.redis_manager import connection
from crdt.model.gcounter import GCounter
from crdt.model.pncounter import PNCounter
from crdt.status_codes import status_codes
from crdt.key_utilities import get_client_list_key, get_client_key


counter_api_blueprint = Blueprint('Counter', __name__)


@counter_api_blueprint.route("/g/new", methods=['GET'])
def new_g_counter():
    key = request.args.get('key')
    client_id = request.args.get('client_id')

    result_dict = dict()

    # Getting all clients and data types of all CRDTs
    all_clients = hot_redis.Set(key=ALL_CLIENTS, client=connection)
    data_types = hot_redis.Dict(key=DATA_TYPES, client=connection)

    # Checking if the client ID is valid
    if client_id not in all_clients:
        print 'Missing Client ID'
        result_dict['status'] = status_codes['client_id_not_found']
        return jsonify(result_dict)

    # Checking if an empty or null key has been given, and generating key
    if key is None or len(key) is 0:
        key = generate_random_crdt_key()
        while key in data_types.keys():
            key = generate_random_crdt_key()
        print 'Generated new random CRDT key'
    # Checking if the key has already been taken
    elif key in data_types.keys() and data_types[key] != G_COUNTER:
            result_dict['status'] = status_codes['data_type_mismatch']
            return jsonify(result_dict)

    # All conditions met for key and client ID
    new_g_counter = GCounter(key=key)
    new_g_counter.add_client(client_id)
    result_dict['status'] = status_codes['success']
    result_dict['key'] = key
    result_dict['data_type'] = data_types[key]
    result_dict['client_id'] = client_id
    return jsonify(result_dict)


@counter_api_blueprint.route("/g/set", methods=['GET'])
def set_g_counter():
    key = request.args.get('key')
    client_id = request.args.get('client_id')
    value = request.args.get('value')

    result_dict = dict()

    check = check_input_fault(key, client_id, value, "default", G_COUNTER)
    if check is False:
        gcounter = GCounter(key=key)
        gcounter.set(client_id, int(value))
        result_dict['status'] = status_codes['success']
        result_dict['value'] = value
        return jsonify(result_dict)
    else:
        result_dict = check
        return jsonify(result_dict)


@counter_api_blueprint.route("/g/get", methods=['GET'])
def get_g_counter():
    key = request.args.get('key')
    client_id = request.args.get('client_id')

    result_dict = dict()

    check = check_input_fault(key, client_id, "default", "default", G_COUNTER)
    if check is False:
        gcounter = GCounter(key=key)
        counter = gcounter.get(client_id)
        result_dict['counter'] = counter
        result_dict['status'] = status_codes['success']
        return jsonify(result_dict)
    else:
        result_dict = check
        return jsonify(result_dict)


@counter_api_blueprint.route("/pn/new", methods=['GET'])
def new_pn_counter():
    key = request.args.get('key')
    client_id = request.args.get('client_id')

    result_dict = dict()

    # Getting all clients and data types of all CRDTs
    all_clients = hot_redis.Set(key=ALL_CLIENTS, client=connection)
    data_types = hot_redis.Dict(key=DATA_TYPES, client=connection)

    # Checking if the client ID is valid
    if client_id not in all_clients:
        print 'Missing Client ID'
        result_dict['status'] = status_codes['client_id_not_found']
        return jsonify(result_dict)

    # Checking if an empty or null key has been given, and generating key
    if key is None or len(key) is 0:
        key = generate_random_crdt_key()
        while key in data_types.keys():
            key = generate_random_crdt_key()
        print 'Generated new random CRDT key'

    # Checking if the key has already been taken
    elif key in data_types.keys() and data_types[key] != PN_COUNTER:
            result_dict['status'] = status_codes['data_type_mismatch']
            return jsonify(result_dict)

    # All conditions met for key and client ID
    new_pn_counter = PNCounter(key=key)
    new_pn_counter.add_client(client_id)
    result_dict['status'] = status_codes['success']
    result_dict['key'] = key
    result_dict['data_type'] = data_types[key]
    result_dict['client_id'] = client_id
    return jsonify(result_dict)


@counter_api_blueprint.route("/pn/set", methods=['GET'])
def set_pn_counter():
    key = request.args.get('key')
    client_id = request.args.get('client_id')
    pvalue = request.args.get('pvalue')
    nvalue = request.args.get('nvalue')

    result_dict = dict()

    check = check_input_fault(key, client_id, pvalue, nvalue, PN_COUNTER)
    if check is False:
        pncounter = PNCounter(key=key)
        pncounter.set(client_id, int(pvalue), int(nvalue))
        result_dict['status'] = status_codes['success']
        result_dict['pvalue'] = pvalue
        result_dict['nvalue'] = nvalue
        return jsonify(result_dict)
    else:
        result_dict = check
        return jsonify(result_dict)


@counter_api_blueprint.route("/pn/get", methods=['GET'])
def get_pn_counter():
    key = request.args.get('key')
    client_id = request.args.get('client_id')

    result_dict = dict()

    check = check_input_fault(key, client_id, "default", "default", PN_COUNTER)
    if check is False:
        pncounter = PNCounter(key=key)
        counter = pncounter.get(client_id)
        result_dict['counter'] = counter
        result_dict['status'] = status_codes['success']
        return jsonify(result_dict)
    else:
        result_dict = check
        return jsonify(result_dict)


def check_input_fault(key, client_id, value1, value2, data_type):
    result_dict = dict()

    # Checking for valid key
    if key is None or len(key) == 0:
        result_dict['status'] = status_codes['missing_key_or_state']
        return result_dict

    # Checking for valid client ID
    if client_id is None or len(client_id) == 0:
        result_dict['status'] = status_codes['client_id_not_found']
        return result_dict

    # Checking for valid value1
    if (value1 is None or len(value1) == 0) and value1 != "default":
        result_dict['status'] = status_codes['value_not_found']
        return result_dict

    # Checking for valid value2
    if (value2 is None or len(value2) == 0) and value2 != "default":
        result_dict['status'] = status_codes['value_not_found']
        return result_dict

    data_types = hot_redis.Dict(key=DATA_TYPES, client=connection)
    all_clients = hot_redis.Set(key=ALL_CLIENTS, client=connection)
    client_list = hot_redis.Set(key=get_client_list_key(key), client=connection)

    # Checking if client ID is valid
    if client_id not in all_clients:
        result_dict['status'] = status_codes['client_id_not_found']
        return result_dict

    # Checking if key is present
    if key not in data_types.keys():
        result_dict['status'] = status_codes['missing_key_or_state']
        return result_dict

    # Checking if the key is the right type
    if data_types[key] != data_type:
        result_dict['status'] = status_codes['data_type_mismatch']
        return result_dict

    # Checking if client is in the GCounter's client list
    if get_client_key(key=key, client_id=client_id) not in client_list:
        result_dict['status'] = status_codes['client_id_not_in_crdt']
        return result_dict

    return False
