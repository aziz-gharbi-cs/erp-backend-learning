import json

from redis import Redis


class CacheService:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get(self, key: str):
        value = self.redis.get(key)

        if value is None:
            return None

        return json.loads(value)

    def set(self, key: str, value, ttl: int = 60):
        self.redis.set(
            key,
            json.dumps(value),
            ex=ttl,
        )

    def delete(self, key: str):
        self.redis.delete(key)