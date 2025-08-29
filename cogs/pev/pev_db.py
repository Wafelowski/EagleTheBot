# pev_db.py
"""
pev_db.py
Reusable MariaDB helper functions using mysql-connector-python.
"""

import mysql.connector, tomli
from mysql.connector import Error
from typing import List, Tuple, Any, Optional

with open("configs/config.toml", "rb") as config:
    DB_CONFIG = tomli.load(config)

# Default connection parameters (can be overridden)
DB_CONFIG = {
    "host": DB_CONFIG["pev_database"]["server"],
    "port": DB_CONFIG["pev_database"]["ports"][0],
    "user": DB_CONFIG["pev_database"]["user"],
    "password": DB_CONFIG["pev_database"]["password"],
    "database": DB_CONFIG["pev_database"]["database"]
}

def get_connection(
    host: str = DB_CONFIG["host"],
    port: int = DB_CONFIG["port"],
    user: str = DB_CONFIG["user"],
    password: str = DB_CONFIG["password"],
    database: str = DB_CONFIG["database"]
) -> mysql.connector.MySQLConnection:
    """
    Create and return a connection to the MariaDB/MySQL database.
    """
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        return conn
    except Error as e:
        raise RuntimeError(f"Error connecting to database: {e}")

def execute_query(
    query: str,
    params: Optional[Tuple[Any, ...]] = None,
    fetch: bool = False
) -> List[Tuple[Any, ...]]:
    """
    Execute a SQL query.
    
    :param query: SQL query string
    :param params: Optional parameters for prepared statements
    :param fetch: If True, fetch and return results (SELECT queries)
    :return: List of tuples with results if fetch=True, otherwise empty list
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(query, params or ())

        if fetch:
            results = cur.fetchall()
        else:
            conn.commit()
            results = []

        return results

    except Error as e:
        conn.rollback()
        raise RuntimeError(f"Query failed: {e}")

    finally:
        cur.close()
        conn.close()

def execute_many(
    query: str,
    params_list: List[Tuple[Any, ...]]
):
    """
    Execute a SQL query multiple times with different parameters (bulk insert/update).
    
    :param query: SQL query string
    :param params_list: List of parameter tuples
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.executemany(query, params_list)
        conn.commit()
    except Error as e:
        conn.rollback()
        raise RuntimeError(f"Bulk query failed: {e}")
    finally:
        cur.close()
        conn.close()
