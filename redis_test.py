import redis

from core.config import settings


client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True,
)


client.set("python:test", "Hello from Python", ex=60)

value = client.get("python:test")

print(value)

print(client.ttl("python:test"))