import hot_redis
from constants import CLIENTS, DATA_TYPES, G_COUNTER
from ..redis_manager import connection


class GCounter:
    def __init__(self, key):
        self.key = key
        self.client_list = hot_redis.Set(key=key+'_'+CLIENTS, client=connection)
        hot_redis.Dict(key=DATA_TYPES)[key] = G_COUNTER

    def add_client(self, client_id):
        new_client = self.key+'_'+client_id
        with hot_redis.transaction():
            for client in self.client_list:
                hot_redis.Dict(key=client, client=connection)[new_client] = 0
            self.client_list.add(new_client)
            new_client_state = hot_redis.Dict(key=new_client)
            for client in self.client_list:
                new_client_state[client] = 0

    def get(self, client_id):
        cur_client = self.key + '_' + client_id
        for client in self.client_list:
            self.merge(cur_client, client)

        cur_client_state = hot_redis.Dict(key=cur_client, client=connection)

        count = 0
        for val in cur_client_state.values():
            count += int(val)

        return count

    def merge(self, client_a, client_b):
        """
        merge client_a with client_b, state of client_a changes
        """
        client_a_state = hot_redis.Dict(key=client_a, client=connection)
        client_b_state = hot_redis.Dict(key=client_b, client=connection)
        for client in self.client_list:
            client_a_state[client] = max(int(client_a_state[client]), int(client_b_state[client]))

    def set(self, client_id, val):
        cur_client = self.key + '_' + client_id
        hot_redis.Dict(key=cur_client, client=connection)[cur_client] = val









