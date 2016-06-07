import hot_redis

from crdt.redis_manager import connection, DATA_TYPES
from crdt.constants import TWO_P_TWO_P_GRAPH
from crdt.key_utilities import get_client_list_key, get_client_key, get_nodes_set_key, get_edges_set_key
from crdt.model.twopset import TwoPSet

class TwoPTwoPGraph:
    def __init__(self, key):
        # Setting the key of the TwoPTwoPGraph Instance
        self.key = key
        self.nodes = TwoPSet(get_nodes_set_key(key))
        self.edges = TwoPSet(get_edges_set_key(key))

        # Getting/Setting the client list and type of the TwoPTwoPGraph instance
        self.client_list = hot_redis.Set(key=get_client_list_key(key), client=connection)
        hot_redis.Dict(key=DATA_TYPES, client=connection)[key] = TWO_P_TWO_P_GRAPH

    def add_client(self, client_id):
        # Adding client ID to client list
        new_client = get_client_key(self.key, client_id)
        self.client_list.add(new_client)

        # Adding clients to component GCounters
        self.nodes.add_client(client_id)
        self.edges.add_client(client_id)

    def set(self, client_id, nodes_add_set, nodes_delete_set, edges_add_set, edges_delete_set):
        self.nodes.set(client_id, nodes_add_set, nodes_delete_set)
        for edge in edges_add_set:
            edge_nodes = edge.split('-')
            if self.nodes.check(edge_nodes[0]) is False or self.nodes.check(edge_nodes[1]) is False:
                edges_add_set.remove(edge)
        self.edges.set(client_id, edges_add_set, edges_delete_set)

