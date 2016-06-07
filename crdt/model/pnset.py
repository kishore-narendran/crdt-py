import hot_redis

from crdt.constants import DATA_TYPES, PN_SET
from crdt.key_utilities import get_client_list_key, get_client_key, get_pncounter_item_pnset_key, get_pnset_key
from crdt.model.pncounter import PNCounter
from crdt.redis_manager import connection


class PNSet:
    def __init__(self, key):
        self.key = key
        self.client_list = hot_redis.Set(key=get_client_list_key(key), client=connection)
        hot_redis.Dict(key=DATA_TYPES, client=connection)[key] = PN_SET
        self.pnset = hot_redis.Set(key=get_pnset_key, client=connection)

    def add_client(self, client_id):
        # Adding client ID to client list
        new_client = get_client_key(self.key, client_id)
        self.client_list.add(new_client)

    def add_client_item(self, client_id, item):
        pn_item_counter = PNCounter(get_pncounter_item_pnset_key(self.key, item))
        if not pn_item_counter.exists(client_id):
            pn_item_counter.add_client(client_id)

    def add(self, client_id, item):
        self.pnset.add(item)
        self.add_client_item(client_id, item)
        PNCounter(get_pncounter_item_pnset_key(self.key, item)).increment(client_id)

    def remove(self, client_id, item):
        self.add_client_item(client_id, item)
        PNCounter(get_pncounter_item_pnset_key(self.key, item)).decrement(client_id)

    def get(self):
        count = set()
        with hot_redis.transaction():  # for consistency
            for item in self.pnset:
                if PNCounter(get_pncounter_item_pnset_key(self.key, item)).get() <= 0:
                    self.pnset.remove(item)  # Garbage Collection
                else:
                    count.add(item)
            return count

    def exists(self, client_id):
        if client_id in self.client_list:
            return True
        else:
            return False
