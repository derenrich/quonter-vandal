
from dataclasses import dataclass
from typing import List
import toolforge
from quonter_vandal.config import DB_NAME


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


class ResultsLogger:
    def __init__(self):
        self._tool_db = toolforge.toolsdb(DB_NAME)

    def log(self, log_line: LogLine):
        with self._tool_db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO results (document, oldrevid, currevid, prediction, data, label)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (log_line.document, log_line.oldrevid,
                 log_line.currevid, log_line.prediction_doc, log_line.data, log_line.label)
            )
        self._tool_db.commit()


class ResultsFetcher:
    def __init__(self):
        self._tool_db = toolforge.toolsdb(DB_NAME)

    def fetch_vandalous(self, limit: int, offset: int) -> List[LogLine]]:
        with self._tool_db.cursor() as cursor:
            cursor.execute(
                """
                SELECT document, oldrevid, currevid, prediction, label, data
                FROM results
                WHERE label = 'True'
                LIMIT %s
                OFFSET %s
                """,
                (limit, offset)
            )
            out = []
            for row in cursor.fetchall():
                out.append(LogLine(*row))
            return out
