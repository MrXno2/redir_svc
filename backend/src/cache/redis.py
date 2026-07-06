from redis.asyncio import Redis

from src.core.settings import settings

redis_engine = Redis.from_url(settings.REDIS_URL, decode_responses=True)

 
class RedisCacheBackend:
    def __init__(
        self, redis: Redis, cache_key: str, cache_ttl_seconds: int | None = None
    ):
        self.redis = redis
        self.cache_ttl_seconds = cache_ttl_seconds
        self.cache_key = cache_key


    async def set(self, key: str, value: str) -> None:
        await self.redis.set(
            self.cache_key + key, value, ex=self.cache_ttl_seconds
        )


    async def get(self, key: str) -> str | None:
        value = await self.redis.get(self.cache_key + key)
        return str(value) if value else None


    async def delete(self, key: str) -> None:
        await self.redis.delete(self.cache_key + key)


redir_cache_redis: RedisCacheBackend = RedisCacheBackend(
    redis=redis_engine, cache_key="redir:", cache_ttl_seconds=3600
)
