from src.core.settings import settings
from redis.asyncio import Redis


redis_engine = Redis.from_url(
    settings.REDIS_URL, 
    decode_responses=True
)


class RedisCacheBackend:
    def __init__(
            self, 
            redis: Redis,
            cache_key: str, 
            cache_ttl_seconds: int | None = None
        ):
        self.redis = redis
        self.cache_ttl_seconds = cache_ttl_seconds
        self.cache_key = cache_key


    async def set(self, key: str, value: str) -> None:
        await self.redis.set(self.cache_key + key, value, ex=self.cache_ttl_seconds) # приводится json к строке


    # если получили строку распарсили, отдали иначе НАНИ
    async def get(self, key: str) -> str | None:
        value = await self.redis.get(self.cache_key + key)
        if value is None:
            return None
        # Если value — bytes, декодируем в str
        elif isinstance(value, bytes):
            return value.decode('utf-8')
        else:
            return str(value)  # На случай, если уже str, обренул чтобы типизация не ругалась


    async def delete(self, key: str) -> None:
        await self.redis.delete(self.cache_key + key)


redir_cache_redis: RedisCacheBackend = RedisCacheBackend(redis=redis_engine,cache_key="redir:", cache_ttl_seconds=3600)



"""
class RedisCacheBackend:
    def __init__(self, redis_url: str, cache_ttl_seconds: int | None = None):
        self.redis = Redis.from_url(redis_url, decoded_responses=True)
        self.cache_ttl_seconds = cache_ttl_seconds

    def set(self, key: str, value: dict) -> None:
        self.redis.set(key, json.dumps(value), ex=self.cache_ttl_seconds) # приводится json к строке

    # если получили строку распарсили, отдали иначе НАНИ
    def get(self, key: str) -> dict | None:
        data = self.redis.get(key)
        return json.loads(data) if data else None

    def delete(self, key: str) -> None:
        self.redis.delete(key)
"""