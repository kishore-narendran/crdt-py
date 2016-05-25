import redis
import hot_redis


class RedisManager:

    redis = None
    connection = None

    def __init__(self):
        # url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
        # self.redis = redis.Redis(host=url.hostname, port=url.port, password=url.password)
        self.redis = redis.Redis(host='localhost', port=6379)
        self.connection = hot_redis.HotClient(host='localhost', port=6379)


redis_manager = RedisManager().redis
connection = RedisManager().connection
