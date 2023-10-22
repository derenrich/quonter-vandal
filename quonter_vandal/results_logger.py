
from dataclasses import dataclass
from typing import List, Self
from quonter_vandal.config import DB_NAME
import os.path
import aiomysql


@dataclass
class LogLine:
    document: str
    oldrevid: int
    currevid: int
    prediction_doc: str
    label: str
    data: str


CREATE_TABLE = """
CREATE OR REPLACE TABLE results (
    id INT NOT NULL AUTO_INCREMENT,
    document VARCHAR(4096) NOT NULL,
    oldrevid INT NOT NULL,
    currevid INT NOT NULL,
    prediction VARCHAR(4096) NOT NULL,
    label varchar(32) NOT NULL,
    data VARCHAR(4096) NOT NULL,
    PRIMARY KEY (id)
);
"""


def build_mysql_args(loop):
    return {
        "read_default_file": os.path.expanduser("~/replica.my.cnf"),
        "charset": "utf8mb4",
        "host": 'tools.db.svc.eqiad.wmflabs',
        "db": DB_NAME,
        "loop": loop,
        "autocommit": True
    }


class ResultsLogger:

    @classmethod
    async def create_logger(cls, loop) -> Self:
        kw = build_mysql_args(loop)
        pool = await aiomysql.create_pool(**kw)  # type: ignore
        return cls(pool)

    def __init__(self, mysql_pool: aiomysql.Pool):
        self._pool = mysql_pool

    async def log(self, log_line: LogLine):
        conn: aiomysql.Connection
        async with self._pool.acquire() as conn:
            cursor: aiomysql.Cursor
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO results (document, oldrevid, currevid, prediction, data, label)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (log_line.document, log_line.oldrevid,
                     log_line.currevid, log_line.prediction_doc, log_line.data, log_line.label)
                )
            if conn:
                await conn.commit()


class ResultsFetcher:
    def __init__(self, pool: aiomysql.Pool):
        self._pool = pool

    @classmethod
    async def create_fetcher(cls, loop) -> Self:
        kw = build_mysql_args(loop)
        pool = await aiomysql.create_pool(**kw)  # type: ignore
        return cls(pool)

    async def fetch_vandalous(self, limit: int, offset: int) -> List[LogLine]:
        conn: aiomysql.Connection
        async with self._pool.acquire() as conn:
            cursor: aiomysql.Cursor
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    SELECT document, oldrevid, currevid, prediction, label, data
                    FROM results
                    WHERE label = 'True'
                    order by currevid desc
                    LIMIT %s
                    OFFSET %s
                    """,
                    (limit, offset)
                )
                out = []
                for row in await cursor.fetchall():
                    out.append(LogLine(*row))
                return out
