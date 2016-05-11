
import random


def generate_random_key():
    key = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
    return key