from core.redis import redis_client
from services.cache_service import CacheService


cache = CacheService(redis_client)

product = {
    "id": 1,
    "reference": "PROD-001",
    "name": "Test Product",
    "stock_quantity": 100,
}

cache.set("product:1", product, ttl=60)

result = cache.get("product:1")

print(result)

cache.delete("product:1")

print(cache.get("product:1"))