import redis
import os
import urlparse


class RedisManager:

    redis = None

    def __init__(self):
        url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
        self.redis = redis.Redis(host=url.hostname, port=url.port, password=url.password)


redis_manager = RedisManager().redis
