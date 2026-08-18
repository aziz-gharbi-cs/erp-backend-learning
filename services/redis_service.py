from core.redis import redis_client


class RedisService:

    @staticmethod
    def set(key: str, value: str, expire: int | None = None) -> None:
        redis_client.set(
            name=key,
            value=value,
            ex=expire,
        )

    @staticmethod
    def get(key: str) -> str | None:
        return redis_client.get(key)

    @staticmethod
    def delete(key: str) -> None:
        redis_client.delete(key)