import hot_redis
from flask import Blueprint, request, jsonify
from crdt.generate_key import generate_random_client_key
from crdt.redis_manager import connection
from crdt.constants import ALL_CLIENTS
from crdt.status_codes import status_codes

client_api_blueprint = Blueprint('Client', __name__)


@client_api_blueprint.route('/new', methods=['GET'])
def create_new_client():
    client_id = request.args.get('client_id')
    result_dict = dict()
    # Getting all client IDs already assigned
    all_clients = hot_redis.Set(key=ALL_CLIENTS, client=connection)

    # Checking if the client id in request is None or an empty string
    if client_id is None or len(client_id) is 0:
        client_id = generate_random_client_key()
        while client_id in all_clients:
            client_id = generate_random_client_key()
    # If client ID in request is valid checking if the client ID is already present
    else:
        if client_id in all_clients:
            result_dict['status'] = status_codes['existing_client_id']
            return jsonify(result_dict)

    # Adding the client ID to the all clients set
    all_clients.add(client_id)
    result_dict['status'] = status_codes['success']
    result_dict['client_id'] = client_id
    return jsonify(result_dict)


