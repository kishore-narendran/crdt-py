import redis
import hot_redis


class RedisManager:

    redis = None

    def __init__(self):
        # url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
        # self.redis = redis.Redis(host=url.hostname, port=url.port, password=url.password)
        self.redis = redis.Redis(host='127.0.0.1', port=6379, db=0)


redis_manager = RedisManager().redis
connection = hot_redis.HotClient(host='localhost', port=6379)