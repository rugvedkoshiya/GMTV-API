from service.redis.redisClient import redisClient


def setCacheData(key, value, expire):
    return redisClient.set(name=key, value=value, ex=expire)


def getCachedata(key):
    return redisClient.get(key)
