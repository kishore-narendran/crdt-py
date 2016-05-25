
import random


def generate_random_crdt_key():
    key = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(16))
    return key


def generate_random_client_key():
    key = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(4))
    return key