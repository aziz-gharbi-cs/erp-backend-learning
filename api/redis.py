from fastapi import APIRouter, Depends
from redis import Redis

from core.dependencies import get_redis

router = APIRouter(
    prefix="/redis",
    tags=["Redis"],
)


@router.get("/test")
def test_redis(redis: Redis = Depends(get_redis)):
    redis.set("api:test", "Hello from FastAPI", ex=60)

    return {
        "value": redis.get("api:test"),
        "ttl": redis.ttl("api:test"),
    }