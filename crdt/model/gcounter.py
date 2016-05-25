import hot_redis

from crdt.constants import CLIENTS, DATA_TYPES, G_COUNTER
from crdt.key_utilities import get_client_list_key, get_client_key
from crdt.redis_manager import connection


class GCounter:
    def __init__(self, key):
        # Setting the key of the GCounter Instance
        self.key = key

        # Getting/Setting the client list and type of the GCounter instance
        self.client_list = hot_redis.Set(key=get_client_list_key(key), client=connection)
        hot_redis.Dict(key=DATA_TYPES, client=connection)[key] = G_COUNTER

    def add_client(self, client_id):
        # Generating a client list key for this key
        new_client = get_client_key(self.key, client_id)
        with hot_redis.transaction():
            # Adding a new state to all the existing clients
            for client in self.client_list:
                hot_redis.Dict(key=client, client=connection)[new_client] = 0

            # Adding client to GCounter instance's client list
            self.client_list.add(new_client)

            # Adding a new state dictionary for this GCounter client
            new_client_state = hot_redis.Dict(key=new_client, client=connection)
            for client in self.client_list:
                new_client_state[client] = 0

    def get(self, client_id):
        # Getting the client's key for this GCounter
        current_client_key = get_client_key(self.key, client_id)

        # Merging state from every other client for this GCounter
        for client in self.client_list:
            self.merge(current_client_key, client)

        # Updating the states from all other clients as the client's latest state
        current_client_state = hot_redis.Dict(key=current_client_key, client=connection)

        # Getting the final merged value
        count = 0
        for val in current_client_state.values():
            count += int(val)

        return count

    def merge(self, client_a, client_b):
        # Getting Client A and Client B's state
        client_a_state = hot_redis.Dict(key=client_a, client=connection)
        client_b_state = hot_redis.Dict(key=client_b, client=connection)

        # Merging Client A's state with Client B's state and storing in Client A's State
        for client in self.client_list:
            client_a_state[client] = max(int(client_a_state[client]), int(client_b_state[client]))

    def set(self, client_id, val):

        # Generating the current client's key for GCounter
        current_client_key = get_client_key(self.key, client_id)

        # Updating the client's state with the value to be set
        hot_redis.Dict(key=current_client_key, client=connection)[current_client_key] = val

