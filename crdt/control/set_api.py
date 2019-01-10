from flask import Blueprint, jsonify, request
from crdt.generate_key import generate_random_crdt_key
from crdt.constants import ALL_CLIENTS, DATA_TYPES, G_SET, TWO_P_SET
from crdt.key_utilities import get_client_list_key, get_client_key
from crdt.model.gset import GSet
from crdt.model.TwoPSet import TwoPSet
from crdt.status_codes import status_codes
from crdt.redis_manager import connection
import hot_redis


set_api_blueprint = Blueprint('Set', __name__)


@set_api_blueprint.route('/g/new', methods=['GET'])
def new_g_set():
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
    elif key in data_types.keys() and data_types[key] != G_SET:
        result_dict['status'] = status_codes['data_type_mismatch']
        return jsonify(result_dict)

    new_g_set = GSet(key=key)
    new_g_set.add_client(client_id)
    result_dict['status'] = status_codes['success']
    result_dict['key'] = key
    result_dict['data_type'] = data_types[key]
    result_dict['client_id'] = client_id
    return jsonify(result_dict)


@set_api_blueprint.route("/g/set", methods=['GET'])
def set_g_set():
    key = request.args.get('key')
    client_id = request.args.get('client_id')
    items = request.args.get('items')

    result_dict = dict()

    check = check_input_fault(key, client_id, G_SET)
    if check is False:
        gset = GSet(key=key)
        gset.set(client_id, items)
        result_dict['status'] = status_codes['success']
        result_dict['items'] = list(eval(items))
        return jsonify(result_dict)
    else:
        result_dict = check
        return jsonify(result_dict)


@set_api_blueprint.route("/g/get", methods=['GET'])
def get_g_set():
    key = request.args.get('key')
    client_id = request.args.get('client_id')

    result_dict = dict()

    check = check_input_fault(key, client_id, G_SET)
    if check is False:
        gset = GSet(key=key)
        counter = gset.get(client_id)
        result_dict['set'] = list(eval(counter))
        result_dict['status'] = status_codes['success']
        return jsonify(result_dict)
    else:
        result_dict = check
        return jsonify(result_dict)


@set_api_blueprint.route('/twop/new', methods=['GET'])
def new_twop_set():
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
    elif key in data_types.keys() and data_types[key] != TWO_P_SET:
        result_dict['status'] = status_codes['data_type_mismatch']
        return jsonify(result_dict)

    new_twop_set = TwoPSet(key=key)
    new_twop_set.add_client(client_id)
    result_dict['status'] = status_codes['success']
    result_dict['key'] = key
    result_dict['data_type'] = data_types[key]
    result_dict['client_id'] = client_id
    return jsonify(result_dict)


@set_api_blueprint.route("/twop/set", methods=['GET'])
def set_twop_set():
    key = request.args.get('key')
    client_id = request.args.get('client_id')
    add_items = request.args.get('add_items')
    delete_items = request.args.get('delete_items')

    result_dict = dict()

    check = check_input_fault(key, client_id, TWO_P_SET)
    if check is False:
        twop_set = TwoPSet(key=key)
        twop_set.set(client_id, add_items, delete_items)
        result_dict['status'] = status_codes['success']
        result_dict['add_items'] = list(eval(add_items))
        result_dict['delete_items'] = list(eval(delete_items))
        return jsonify(result_dict)
    else:
        result_dict = check
        return jsonify(result_dict)


@set_api_blueprint.route("/twop/check", methods=['GET'])
def check_twop_set():
    key = request.args.get('key')
    client_id = request.args.get('client_id')
    item = request.args.get('item')

    result_dict = dict()

    check = check_input_fault(key, client_id, TWO_P_SET)
    if check is False:
        twop_set = TwoPSet(key=key)
        is_found = twop_set.check(client_id, item)
        result_dict['status'] = status_codes['success']
        result_dict['found'] = is_found
        return jsonify(result_dict)
    else:
        result_dict = check
        return jsonify(result_dict)


@set_api_blueprint.route("/twop/get", methods=['GET'])
def get_twop_set():
    key = request.args.get('key')
    client_id = request.args.get('client_id')

    result_dict = dict()

    check = check_input_fault(key, client_id, TWO_P_SET)
    if check is False:
        twop_set = TwoPSet(key=key)
        result_set = twop_set.get(client_id)
        result_dict['set'] = list(eval(result_set))
        result_dict['status'] = status_codes['success']
        return jsonify(result_dict)
    else:
        result_dict = check
        return jsonify(result_dict)


def check_input_fault(key, client_id, data_type):
    result_dict = dict()

    # Checking for valid key
    if key is None or len(key) == 0:
        result_dict['status'] = status_codes['missing_key_or_state']
        return result_dict

    # Checking for valid client ID
    if client_id is None or len(client_id) == 0:
        result_dict['status'] = status_codes['client_id_not_found']
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
