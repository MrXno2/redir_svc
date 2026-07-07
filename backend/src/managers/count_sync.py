"""

import asyncio

from sqlalchemy import update

from src.cache.redis import redir_count_cache_redis
from src.core.logger import logger
from src.db.models.redir import RedirModel
from src.db.session import AsyncSessionLocal

SYNC_INTERVAL = 300  # 5 минут


async def count_sync_manager():
    while True:
        try:
            await _sync_counts_to_db()
        except Exception:
            logger.exception("Count sync manager error")
        await asyncio.sleep(SYNC_INTERVAL)


async def _sync_counts_to_db():
    cache = redir_count_cache_redis
    counts: dict[str, int] = {}

    cursor = 0
    while True:
        cursor, keys = await cache.redis.scan(
            cursor, match=f"{cache.cache_key}*", count=100
        )
        for raw_key in keys:
            key = raw_key.removeprefix(cache.cache_key)
            value = await cache.get(key)
            if value is not None:
                counts[key] = int(value)
                await cache.delete(key)
        if cursor == 0:
            break

    if not counts:
        return

    async with AsyncSessionLocal() as session:
        async with session.begin():
            for redir_url, count in counts.items():
                await session.execute(
                    update(RedirModel)
                    .where(RedirModel.redir_url == redir_url)
                    .values(redir_count=RedirModel.redir_count + count)
                )

    logger.info(f"Synced {len(counts)} redirect counts to DB")
    
"""