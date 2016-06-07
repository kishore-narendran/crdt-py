import hot_redis
from crdt.constants import LWW_REGISTER, DATA_TYPES
from crdt.redis_manager import connection
from crdt.key_utilities import get_client_key, get_client_list_key


class LWWERegister:
    def __init__(self, key):
        # Setting the key of the LWWERegister Instance
        self.key = key

        # Getting/Setting the client list and type of the LWWERegister instance
        self.client_list = hot_redis.Set(key=get_client_list_key(key), client=connection)
        hot_redis.Dict(key=DATA_TYPES, client=connection)[key] = LWW_REGISTER

    def add_client(self, client_id):
        # Generating a client list key for this key
        new_client = get_client_key(self.key, client_id)

        with hot_redis.transaction():
            # Adding a new state to all the existing clients
            for client in self.client_list:
                hot_redis.Dict(key=client, client=connection)[new_client] = str({'timestamp': -1, 'value': None})

            # Adding client to LWWERegister instance's client list
            self.client_list.add(new_client)

            # Adding a new state dictionary for this LWWERegister client
            new_client_state = hot_redis.Dict(key=new_client, client=connection)
            for client in self.client_list:
                new_client_state[client] = str({'timestamp': -1, 'value': None})

    def set(self, client_id, val, timestamp):

        # Generating the current client's key for LWWERegister
        current_client_key = get_client_key(self.key, client_id)

        # Updating the client's state with the value to be set
        hot_redis.Dict(key=current_client_key, client=connection)[current_client_key] = str({'value': val, 'timestamp':
                                                                                             timestamp})

    def get(self, client_id):
        # Getting the client's key for this LWWERegister
        current_client_key = get_client_key(self.key, client_id)

        # Merging state from every other client for this LWWERegister
        for client in self.client_list:
            self.merge(current_client_key, client)

        # Updating the states from all other clients as the client's latest state
        current_client_state = hot_redis.Dict(key=current_client_key, client=connection)

        register = dict()
        register['value'] = eval(current_client_state[current_client_key])['value']
        register['timestamp'] = eval(current_client_state[current_client_key])['timestamp']
        for value in current_client_state.values():
            value = eval(value)
            if value['timestamp'] > register['timestamp']:
                register['value'] = value['value']
                register['timestamp'] = value['timestamp']

        current_client_state[current_client_key] = str(register)
        return str(register)

    def merge(self, client_a, client_b):
        # Getting Client A and Client B's state
        client_a_state = hot_redis.Dict(key=client_a, client=connection)
        client_b_state = hot_redis.Dict(key=client_b, client=connection)

        # Merging Client A's state with Client B's state and storing in Client A's State
        for client in self.client_list:
            client_a_value = eval(client_a_state[client])
            client_b_value = eval(client_b_state[client])
            if client_a_value['timestamp'] > client_b_value['timestamp']:
                client_a_state[client] = str({'value': client_a_value['value'],
                                              'timestamp': client_a_value['timestamp']})
            else:
                client_a_state[client] = str({'value': client_b_value['value'],
                                              'timestamp': client_b_value['timestamp']})

