import redis

# redisClient = redis.Redis(
#     host='127.0.0.1',
#     port=6379, 
# )

redisClient = redis.Redis.from_url("redis://redis:6379/0")