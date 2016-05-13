import redis


class RedisManager:

    redis = None

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)


redis_manager = RedisManager().redis
