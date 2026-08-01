# pev_db.py
"""
pev_db.py
Reusable MariaDB helper functions using aiomysql (async).
"""

import aiomysql, tomli, asyncio
from typing import List, Tuple, Any, Optional
from datetime import datetime, date, time


with open("configs/config.toml", "rb") as config:
    DB_CONFIG = tomli.load(config)

DB_CONFIG = {
    "host": DB_CONFIG["pev_database"]["server"],
    "port": DB_CONFIG["pev_database"]["ports"][0],
    "user": DB_CONFIG["pev_database"]["user"],
    "password": DB_CONFIG["pev_database"]["password"],
    "db": DB_CONFIG["pev_database"]["database"]
}

async def get_connection(
    host: str = DB_CONFIG["host"],
    port: int = DB_CONFIG["port"],
    user: str = DB_CONFIG["user"],
    password: str = DB_CONFIG["password"],
    db: str = DB_CONFIG["db"]
) -> aiomysql.Connection:
    """
    Create and return an async connection to the MariaDB/MySQL database.
    """
    try:
        conn = await aiomysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            db=db,
            autocommit=True
        )
        return conn
    except Exception as e:
        raise RuntimeError(f"Error connecting to database: {e}")

async def execute_query(
    query: str,
    params: Optional[Tuple[Any, ...]] = None,
    fetch: bool = False
) -> List[Tuple[Any, ...]]:
    """
    Execute a SQL query asynchronously.

    :param query: SQL query string
    :param params: Optional parameters for prepared statements
    :param fetch: If True, fetch and return results (SELECT queries)
    :return: List of tuples with results if fetch=True, otherwise empty list
    """
    conn = await get_connection()
    async with conn.cursor() as cur:
        try:
            await cur.execute(query, params or ())
            if fetch:
                results = await cur.fetchall()
            else:
                await conn.commit()
                results = []
            return results
        except Exception as e:
            await conn.rollback()
            raise RuntimeError(f"Query failed: {e}")
        finally:
            conn.close()

async def execute_many(
    query: str,
    params_list: List[Tuple[Any, ...]]
):
    """
    Execute a SQL query multiple times with different parameters (bulk insert/update) asynchronously.

    :param query: SQL query string
    :param params_list: List of parameter tuples
    """
    conn = await get_connection()
    async with conn.cursor() as cur:
        try:
            await cur.executemany(query, params_list)
            await conn.commit()
        except Exception as e:
            await conn.rollback()
            raise RuntimeError(f"Bulk query failed: {e}")
        finally:
            conn.close()

def date_cnvrt(value: datetime | date):
    """Convert datetime/date values to a display-friendly string."""
    if isinstance(value, datetime):
        return value.strftime("%d-%m-%Y %H:%M:%S")
    if isinstance(value, date):
        return value.strftime("%d-%m-%Y")
    return value
