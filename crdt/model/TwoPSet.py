import hot_redis

from crdt.constants import DATA_TYPES, TWO_P_SET
from crdt.key_utilities import get_client_list_key, get_client_key, get_add_set_key, get_delete_set_key
from crdt.redis_manager import connection
from crdt.model.gset import GSet
from random import random


class TwoPSet:
    def __init__(self, key):
        # Setting the key of the PN Counter Instance
        self.key = key
        self.add_set = GSet(get_add_set_key(key))
        self.delete_set = GSet(get_delete_set_key(key))

        # Getting/Setting the client list and type of the GCounter instance
        self.client_list = hot_redis.Set(key=get_client_list_key(key), client=connection)
        hot_redis.Dict(key=DATA_TYPES, client=connection)[key] = TWO_P_SET

    def add_client(self, client_id):
        # Adding client ID to client list
        new_client = get_client_key(self.key, client_id)
        self.client_list.add(new_client)

        # Adding clients to component GCounters
        self.add_set.add_client(client_id)
        self.delete_set.add_client(client_id)

    def get(self, client_id):
        add_set_value = self.add_set.get(client_id)
        delete_set_value = self.delete_set.get(client_id)
        final_set = eval(add_set_value).difference(eval(delete_set_value))
        return repr(final_set)

    def check(self, val, client_id=None):
        if client_id is None:
            final_set = self.get(self, random.choice(list(self.client_list)))
        else:
            final_set = self.get(self, client_id)
        final_set = eval(final_set)
        if val in final_set:
            return True
        else:
            return False

    def set(self, client_id, add_set, delete_set):
        self.add_set.set(client_id, add_set)
        self.delete_set.set(client_id, delete_set)

