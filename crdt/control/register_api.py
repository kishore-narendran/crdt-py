import hot_redis
from flask import Blueprint, request, jsonify

from crdt.constants import DATA_TYPES, LWW_REGISTER, ALL_CLIENTS
from crdt.generate_key import generate_random_crdt_key
from crdt.redis_manager import connection
from crdt.model.lwwregister import LWWERegister
from crdt.status_codes import status_codes
from crdt.key_utilities import get_client_list_key, get_client_key


register_api_blueprint = Blueprint('Register', __name__)


@register_api_blueprint.route('/lwwe/new', methods=['GET'])
def new_lwwe_register():
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
    elif key in data_types.keys() and data_types[key] != LWW_REGISTER:
        result_dict['status'] = status_codes['data_type_mismatch']
        return jsonify(result_dict)

    new_lwwe_register = LWWERegister(key=key)
    new_lwwe_register.add_client(client_id)
    result_dict['status'] = status_codes['success']
    result_dict['key'] = key
    result_dict['data_type'] = data_types[key]
    result_dict['client_id'] = client_id
    return jsonify(result_dict)


@register_api_blueprint.route("/lwwe/set", methods=['GET'])
def set_lwwe_register():
    key = request.args.get('key')
    client_id = request.args.get('client_id')
    value = request.args.get('value')
    timestamp = request.args.get('timestamp')

    result_dict = dict()

    check = check_input_fault(key, client_id, timestamp, LWW_REGISTER)
    if check is False:
        timestamp = float(timestamp)
        lwweregister = LWWERegister(key=key)
        lwweregister.set(client_id, value, timestamp)
        result_dict['status'] = status_codes['success']
        result_dict['value'] = value
        result_dict['timestamp'] = timestamp
        return jsonify(result_dict)
    else:
        result_dict = check
        return jsonify(result_dict)


@register_api_blueprint.route("/lwwe/get", methods=['GET'])
def get_lwwe_register():
    key = request.args.get('key')
    client_id = request.args.get('client_id')

    result_dict = dict()

    check = check_input_fault(key, client_id, -1.0, LWW_REGISTER)
    if check is False:
        lwweregister = LWWERegister(key=key)
        register_value = lwweregister.get(client_id)
        result_dict['value'] = eval(register_value)['value']
        result_dict['timestamp'] = eval(register_value)['timestamp']
        result_dict['status'] = status_codes['success']
        return jsonify(result_dict)
    else:
        result_dict = check
        return jsonify(result_dict)


def check_input_fault(key, client_id, timestamp, data_type):
    result_dict = dict()

    # Checking for valid key
    if key is None or len(key) == 0:
        result_dict['status'] = status_codes['missing_key_or_state']
        return result_dict

    # Checking for valid client ID
    if client_id is None or len(client_id) == 0:
        result_dict['status'] = status_codes['client_id_not_found']
        return result_dict

    # Checking validity of timestamp
    if timestamp != -1.0:
        try:
            timestamp = float(timestamp)
        except ValueError:
            result_dict['status'] = status_codes['timestamp_not_valid']
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