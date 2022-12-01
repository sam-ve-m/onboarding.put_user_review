# Standards
from contextlib import asynccontextmanager

# Third party
from decouple import config
import cx_Oracle_async


class OracleInfrastructure:

    pool = None

    @classmethod
    async def _get_pool(cls):
        if cls.pool is None:
            cls.pool = await cx_Oracle_async.create_pool(
                config("ORACLE_CONNECTION_STRING"),
                min=2,
                max=100,
                increment=1
            )
        return cls.pool

    @classmethod
    @asynccontextmanager
    async def get_connection(cls):
        pool = await cls._get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                yield cursor
                await conn.commit()
